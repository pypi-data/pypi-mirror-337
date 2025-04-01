import os
import json
import asyncio
import yaml
from datetime import datetime

import tornado.web
import tornado.ioloop
import tornado.httpclient

import boto3
from botocore.exceptions import ClientError
from botocore import UNSIGNED
from botocore.config import Config

import time
from sqlalchemy import create_engine, Column, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from jupyter_server.base.handlers import APIHandler


# -----------------------------------------------------------
# Configuración de SQLAlchemy para el caché de buckets públicos
# -----------------------------------------------------------
Base = declarative_base()


class Cache(Base):
    __tablename__ = "cache_table"
    cache_key = Column(String, primary_key=True)
    value = Column(Text)  # Se guardará el JSON serializado como texto
    timestamp = Column(Float)


engine = create_engine(
    "sqlite:///cache.db", echo=False, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base.metadata.create_all(bind=engine)

# TTL para el caché (por defecto 5 minutos)
_CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
# URL para descargar la lista de buckets públicos (configurable vía variable de entorno)
PUBLIC_BUCKETS_URL = os.getenv(
    "PUBLIC_BUCKETS_URL",
    "https://api.github.com/repos/awslabs/open-data-registry/contents/datasets",
)
# Directorio local para guardar descargas
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR", "tmp")


def _set_cache(key, value):
    """
    Guarda el valor en la caché. Se serializa el objeto 'value' a JSON para almacenarlo como texto.
    """
    try:
        serialized_value = json.dumps(value)  # Serializamos el dict a JSON
        timestamp = time.time()
        # Buscamos si ya existe un registro con la misma key
        cache_entry = session.query(Cache).filter_by(cache_key=key).first()
        if cache_entry:
            cache_entry.value = serialized_value
            cache_entry.timestamp = timestamp
        else:
            cache_entry = Cache(
                cache_key=key, value=serialized_value, timestamp=timestamp
            )
            session.add(cache_entry)
        session.commit()
    except Exception as e:
        print("Error guardando en caché:", e)
        session.rollback()


def _get_from_cache(key):
    """
    Recupera el valor de la caché y lo deserializa de JSON a dict.
    """
    try:
        cache_entry = session.query(Cache).filter_by(cache_key=key).first()
        if cache_entry:
            if time.time() - cache_entry.timestamp < _CACHE_TTL:
                return json.loads(cache_entry.value)  # Deserializamos el JSON a dict
        return None
    except Exception as e:
        print("Error obteniendo desde la caché:", e)
        return None


# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------
def get_s3_client(client_type="private"):
    """
    Devuelve el cliente S3 adecuado.
    Para 'private' se usa el cliente autenticado (tomando credenciales del sistema).
    Para 'public' se usa un cliente sin firma.
    """
    if client_type == "public":
        return boto3.client("s3", config=Config(signature_version=UNSIGNED))
    else:
        # return boto3.client("s3")
        session = boto3.Session()
        return session.client("s3")


def formato_tamano(bytes):
    """Convierte bytes a KB, MB, GB según el tamaño"""
    for unidad in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unidad}"
        bytes /= 1024.0


def format_item(
    name, is_file, path, has_child, item_type, size=0, date_modified="", region=""
):
    """
    Formatea un item (archivo o carpeta) según lo espera FileManager.
    """
    return {
        "name": name,
        "isFile": is_file,
        "path": path,
        "hasChild": has_child,
        "type": item_type,
        "size": formato_tamano(size) if size != "-" and size != "" else size,
        "dateModified": (
            datetime.fromisoformat(date_modified).strftime("%b %d, %Y")
            if date_modified != "-" and date_modified != ""
            else date_modified
        ),
        "region": region,
    }


def list_bucket_contents(s3_client, bucket_name, prefix):
    """
    Lista el contenido interno de un bucket dado el bucket y un prefijo.
    Devuelve una lista combinada de carpetas y archivos.
    """
    all_files = []
    all_folders = []
    continuation_token = None
    while True:
        # Obtener la región del bucket
        # location = s3_client.get_bucket_location(Bucket=bucket_name)[
        #     "LocationConstraint"
        # ]
        location = "us-east-1"
        region = location if location else "us-east-1"

        list_params = {"Bucket": bucket_name, "Prefix": prefix, "Delimiter": "/"}
        if continuation_token:
            list_params["ContinuationToken"] = continuation_token

        response = s3_client.list_objects_v2(**list_params)

        # Procesar archivos (omitimos el objeto que define la carpeta)
        for obj in response.get("Contents", []):
            key = obj.get("Key", "")
            if key == prefix:
                continue
            file_name = key.split("/")[-1]
            size = obj.get("Size", 0)
            last_modified = obj.get("LastModified")
            date_modified = last_modified.isoformat() if last_modified else ""
            all_files.append(
                format_item(
                    file_name,
                    True,
                    f"/{bucket_name}/{key}",
                    False,
                    "file",
                    size,
                    date_modified,
                    region=region,
                )
            )

        # Procesar carpetas
        for common_prefix in response.get("CommonPrefixes", []):
            folder_prefix = common_prefix.get("Prefix", "")
            folder_name = folder_prefix.rstrip("/").split("/")[-1]
            all_folders.append(
                format_item(
                    folder_name,
                    False,
                    f"/{bucket_name}/{folder_prefix}",
                    True,
                    "folder",
                    size="-",
                    date_modified="-",
                    region=region,
                )
            )

        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    return all_folders + all_files


class BaseHandler(APIHandler):
    def set_default_headers(self):
        # Allow any domain to access your API
        self.set_header("Access-Control-Allow-Origin", "*")
        # List the allowed headers
        self.set_header(
            "Access-Control-Allow-Headers",
            "x-requested-with, content-type, Authorization",
        )
        # List the allowed methods
        self.set_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )

    # Handle OPTIONS requests
    def options(self, *args, **kwargs):
        # no body is sent for an OPTIONS request
        self.set_status(204)
        self.finish()


# -----------------------------------------------------------
# Handler Unificado para FileManager (operaciones: read, download, details)
# -----------------------------------------------------------
class FileManagerHandler(BaseHandler):
    def set_default_headers(self):
        # Permitir todos los orígenes (para pruebas; en producción, especifica el dominio adecuado)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    # @tornado.web.authenticated
    async def post(self):
        # Parseamos la solicitud JSON
        try:
            # data = json.loads(self.request.body) if self.request.body else {}

            content_type = self.request.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data = json.loads(self.request.body.decode("utf-8"))
            else:
                # Si se envía en formato URL-encoded, se usa get_argument
                # Por ejemplo, para la acción "download" se espera recibir "downloadInput"
                download_input_raw = self.get_argument("downloadInput", None)
                # Si no se recibió "downloadInput", intentar parsear el body completo
                if download_input_raw is None:
                    data = json.loads(self.request.body.decode("utf-8"))
                else:
                    # Aquí, data solo tendrá la clave "downloadInput"
                    data = json.loads(download_input_raw)

        except Exception as e:
            self.set_status(400)
            self.write({"error": "Error en el parseo del JSON: " + str(e)})
            return

        print(f"Datos recibidos: {data}")
        action = data.get("action", "").lower()
        print(f"Acción solicitada: {action}")
        path = data.get("path", "").strip()  # Ej: "/bucket_name/optional_prefix"
        # client_type determina si se opera sobre buckets "private" o "public"
        client_type = data.get("client_type", "public").lower()
        s3_client = get_s3_client(client_type)

        if action == "read":
            # Si no se especifica path (raíz) se listan los buckets
            if not path or path == "/":
                if client_type == "private":
                    result = self._list_private_buckets(s3_client)
                else:
                    result = await self._list_public_buckets()
                self.set_header("Content-Type", "application/json")
                self.write(result)
            else:
                # Listar contenido interno de un bucket (público o privado)
                result = self._list_bucket_contents(s3_client, path, client_type)
                self.set_header("Content-Type", "application/json")
                self.write(result)
        elif action == "download":
            self._download_file(data, s3_client)
        elif action == "details":
            self._get_details(data, s3_client)
        elif action == "search":
            result = await self._search_items(data, s3_client, client_type)
            self.set_header("Content-Type", "application/json")
            self.write(result)
        else:
            self.set_status(400)
            self.write({"error": "Acción no soportada"})

    def _list_private_buckets(self, s3_client):
        """
        Listado de buckets privados usando list_buckets.
        """
        try:
            cache_key = "private_buckets"
            cached_result = _get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result

        except Exception as e:
            self.application.settings.get("logger", print)(
                f"Error al acceder a cache: {e}"
            )

        try:
            response = s3_client.list_buckets()
            buckets = []
            for bucket in response.get("Buckets", []):
                name = bucket.get("Name")
                # location = s3_client.get_bucket_location(Bucket=name)[
                #     "LocationConstraint"
                # ]
                location = "us-east-1"
                region = location if location else "us-east-1"
                buckets.append(
                    format_item(
                        name,
                        False,
                        f"/{name}/",
                        True,
                        "folder",
                        size="-",
                        date_modified="-",
                        region=region,
                    )
                )

            cwd = format_item("Root", False, "/", True, "folder")
            result = {"cwd": cwd, "files": buckets}
            try:
                _set_cache(cache_key, result)
            except Exception as e:
                print(f"Error guardando en caché: {e}")
            finally:
                session.close()

            return json.dumps(result)
        except ClientError as e:
            self.set_status(403)
            return json.dumps(
                {"error": "No tienes permisos para acceder a los buckets privados: {e}"}
            )
        except Exception as e:
            self.set_status(500)
            return json.dumps({"error": str(e)})

    async def _list_public_buckets(self):
        """
        Obtiene la lista de buckets públicos a partir de un archivo JSON (descargado y cacheado).
        """
        try:
            cache_key = "public_buckets"
            cached_result = _get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result

        except Exception as e:
            self.application.settings.get("logger", print)(
                f"Error al acceder a cache: {e}"
            )

        # Si no hay caché o ha caducado, procedemos a obtener los datos
        http_client = tornado.httpclient.AsyncHTTPClient()
        datasets_url = PUBLIC_BUCKETS_URL

        try:
            response = await http_client.fetch(datasets_url)
            datasets = json.loads(response.body.decode())
        except Exception as e:
            self.set_status(500)
            self.write({"error": f"Error al obtener la lista de datasets: {e}"})
            return

        # Realizamos las peticiones en paralelo para cada archivo YAML
        tasks = []
        for item in datasets:
            download_url = item.get("download_url")
            if download_url:
                tasks.append(
                    self.fetch_and_process_yaml(
                        http_client, download_url, item.get("name")
                    )
                )

        results = await asyncio.gather(*tasks, return_exceptions=True)
        final_results = []
        for res in results:
            if isinstance(res, Exception):
                self.application.settings.get("logger", print)(f"Error en tarea: {res}")
            elif res:
                final_results.append(res)

        flattened = [obj for sublist in final_results for obj in sublist]

        try:
            result = {
                "cwd": {
                    "name": "Root",
                    "isFile": False,
                    "path": "/",
                    "hasChild": True,
                    "type": "folder",
                    "size": "-",
                    "dateModified": "-",
                },
                "files": flattened,
            }
            try:
                _set_cache(cache_key, result)
            except Exception as e:
                print(f"Error guardando en caché: {e}")
            finally:
                session.close()
            return result
        except Exception as e:
            self.set_status(500)
            return json.dumps(
                {"error": "Error al descargar buckets públicos: " + str(e)}
            )

    def extract_bucket_name(self, arn: str) -> str:
        """
        Extrae el nombre del bucket a partir de su ARN.
        Se elimina el prefijo "arn:aws:s3:::" y se divide la cadena por "/".
        Se toma el último componente no vacío.
        """
        if not arn:
            return ""
        prefix = "arn:aws:s3:::"
        if arn.startswith(prefix):
            arn = arn[len(prefix) :]
        parts = [p for p in arn.split("/") if p]
        return parts[-1] if parts else arn

    async def fetch_and_process_yaml(self, http_client, url, filename):
        """
        Descarga el archivo YAML, procesa la sección 'Resources' y extrae los buckets S3.
        """
        try:
            response = await http_client.fetch(url)
            yaml_text = response.body.decode()
            data = yaml.safe_load(yaml_text)
        except Exception as e:
            return {"file": filename, "error": str(e)}

        resources = data.get("Resources", [])
        buckets = [
            {
                "Description": resource.get("Description"),
                "ARN": resource.get("ARN"),
                "Region": resource.get("Region"),
                "Type": resource.get("Type"),
            }
            for resource in resources
            if "s3 bucket" in resource.get("Type", "").lower()
        ]

        files_list = []
        # Para cada recurso, se filtra si es un bucket S3 y se procesa
        for bucket in buckets:
            # Se asumen que el ARN se encuentra directamente en el objeto
            arn = bucket.get("ARN")
            if not arn:
                continue
            bucket_name = self.extract_bucket_name(arn)
            bucket_region = bucket.get("Region")
            file_obj = {
                "name": bucket_name,
                "isFile": False,
                "path": f"/{bucket_name}/",
                "hasChild": True,
                "type": "folder",
                "size": "-",
                "dateModified": "-",
                "region": bucket_region,
            }
            files_list.append(file_obj)

        return files_list

    def _list_bucket_contents(self, s3_client, path, client_type):
        """
        Lista el contenido interno de un bucket dado el path.
        Para privados, verifica acceso mediante head_bucket.
        """
        sanitized = path.lstrip("/")
        parts = sanitized.split("/", 1)
        bucket_name = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""
        if client_type == "private":
            try:
                s3_client.head_bucket(Bucket=bucket_name)
            except ClientError:
                self.set_status(403)
                return json.dumps(
                    {
                        "error": f"No tienes permisos para acceder al bucket {bucket_name}."
                    }
                )
        try:
            items = list_bucket_contents(s3_client, bucket_name, prefix)
            cwd_name = prefix.split("/")[-1] if prefix else bucket_name
            cwd_path = f"/{bucket_name}/{prefix}".rstrip("/")
            if not cwd_path:
                cwd_path = f"/{bucket_name}/"
            cwd = format_item(cwd_name, False, cwd_path, True, "folder")
            return json.dumps({"cwd": cwd, "files": items})
        except Exception as e:
            self.set_status(500)
            return json.dumps({"error": str(e)})

    def _download_file(self, data, s3_client):
        """
        Descarga un archivo usando get_object de S3 y lo guarda localmente.
        La solicitud debe incluir 'downloadsFolder' y la información del archivo en 'data'.
        """
        try:
            downloads_folder = data.get("downloadsFolder", DOWNLOADS_DIR)
            if data.get("data") and len(data.get("data")) > 0:
                file_full_path = data["data"][0].get("path")
            else:
                file_full_path = os.path.join(
                    data.get("path", ""), data.get("names", [""])[0]
                )
            file_path = file_full_path.strip("/")
            parts = file_path.split("/", 1)
            if len(parts) < 2:
                self.set_status(400)
                self.write(
                    json.dumps(
                        {
                            "error": "La ruta del archivo debe tener el formato 'bucket/key'"
                        }
                    )
                )
                return
            bucket_name, key = parts
            response = s3_client.get_object(Bucket=bucket_name, Key=key)
            file_content = response["Body"].read()
            os.makedirs(downloads_folder, exist_ok=True)
            local_file_path = os.path.join(downloads_folder, os.path.basename(key))
            with open(local_file_path, "wb") as f:
                f.write(file_content)
            self.write(json.dumps({"success": True, "file_saved": local_file_path}))
        except ClientError:
            self.set_status(403)
            self.write(
                json.dumps({"error": "No tienes permisos para descargar este archivo."})
            )
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

    def _get_details(self, data, s3_client):
        """
        Obtiene detalles de un archivo o carpeta.
        """
        try:
            items = data.get("data", [])
            if not items:
                self.set_status(400)
                self.write(json.dumps({"error": "El parámetro 'data' es requerido."}))
                return
            details = []
            for item in items:
                full_path = item.get("path", "").strip("/")
                if not full_path:
                    continue
                parts = full_path.split("/", 1)
                bucket_name = parts[0]
                object_key = parts[1] if len(parts) > 1 else ""
                try:
                    if s3_client.meta.config.signature_version != UNSIGNED:
                        s3_client.head_bucket(Bucket=bucket_name)
                except ClientError:
                    self.set_status(403)
                    self.write(
                        json.dumps(
                            {
                                "error": f"No tienes permisos para acceder al bucket {bucket_name}."
                            }
                        )
                    )
                    return
                if not object_key or object_key.endswith("/"):
                    folder_detail = format_item(
                        item.get("name"),
                        False,
                        f"/{bucket_name}/{object_key}",
                        True,
                        "folder",
                    )
                    details.append(folder_detail)
                else:
                    try:
                        response = s3_client.head_object(
                            Bucket=bucket_name, Key=object_key
                        )
                        last_modified = response.get("LastModified")
                        date_mod_str = (
                            last_modified.isoformat() if last_modified else ""
                        )
                        file_detail = format_item(
                            item.get("name"),
                            True,
                            f"/{bucket_name}/{object_key}",
                            False,
                            "file",
                            response.get("ContentLength", 0),
                            date_mod_str,
                        )
                        details.append(file_detail)
                    except ClientError as e:
                        code = e.response["Error"]["Code"]
                        if code in ["404", "NoSuchKey"]:
                            folder_detail = format_item(
                                item.get("name"),
                                False,
                                f"/{bucket_name}/{object_key}/",
                                True,
                                "folder",
                            )
                            details.append(folder_detail)
                        else:
                            self.set_status(403)
                            self.write(
                                json.dumps(
                                    {
                                        "error": f"No tienes permisos para acceder al objeto {object_key}."
                                    }
                                )
                            )
                            return
            self.write(json.dumps({"details": details[0] if details else {}}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": "Error interno del servidor: " + str(e)}))

    async def _search_items(self, data, s3_client, client_type):
        """
        Realiza la operación de búsqueda.
        - Si se busca en la raíz (path vacío): filtra los buckets (privados o públicos).
        - Si se busca dentro de un bucket: filtra los objetos y carpetas que contengan el texto.
        Se espera que el parámetro 'searchString' esté presente.
        """
        # search_text = data.get("searchString", "").strip().lower()
        search_text = data.get("searchString", "").replace("*", "").lower()

        if not search_text:
            self.set_status(400)
            return json.dumps({"error": "El parámetro 'searchString' es requerido."})

        path = data.get("path", "").strip()

        # Caso: búsqueda en la raíz
        if not path or path == "/":
            if client_type == "private":
                try:
                    response = s3_client.list_buckets()
                    buckets = []
                    for bucket in response.get("Buckets", []):
                        name = bucket.get("Name", "")
                        if search_text in name.lower():
                            buckets.append(
                                format_item(name, False, f"/{name}/", True, "folder")
                            )
                    cwd = format_item("Root", False, "/", True, "folder")
                    return json.dumps({"cwd": cwd, "files": buckets})
                except Exception as e:
                    self.set_status(500)
                    return json.dumps({"error": str(e)})
            else:
                # Para públicos: usar el listado cacheado y filtrar
                public_buckets_str = await self._list_public_buckets()
                try:

                    if not isinstance(public_buckets_str, dict):
                        public_buckets_data = json.loads(public_buckets_str)
                    else:
                        public_buckets_data = public_buckets_str
                except Exception as e:
                    self.set_status(500)
                    return json.dumps(
                        {
                            "error": "Error al parsear el listado de buckets públicos: "
                            + str(e)
                        }
                    )
                filtered = [
                    item
                    for item in public_buckets_data.get("files", [])
                    if search_text in item.get("name", "").lower()
                ]
                cwd = public_buckets_data.get(
                    "cwd", format_item("Root", False, "/", True, "folder")
                )
                return json.dumps({"cwd": cwd, "files": filtered})
        else:
            # Búsqueda dentro de un bucket o carpeta
            sanitized = path.lstrip("/")
            parts = sanitized.split("/", 1)
            bucket_name = parts[0]
            prefix = parts[1] if len(parts) > 1 else ""
            try:
                if client_type == "private":
                    try:
                        s3_client.head_bucket(Bucket=bucket_name)
                    except ClientError:
                        self.set_status(403)
                        return json.dumps(
                            {
                                "error": f"No tienes permisos para acceder al bucket {bucket_name}."
                            }
                        )
                list_params = {
                    "Bucket": bucket_name,
                    "Prefix": prefix,
                    "Delimiter": "/",
                }
                response = s3_client.list_objects_v2(**list_params)
                matching_files = []
                matching_folders = []
                for obj in response.get("Contents", []):
                    key = obj.get("Key", "")
                    if search_text in key.lower():
                        file_name = key.split("/")[-1]
                        size = obj.get("Size", 0)
                        last_modified = obj.get("LastModified")
                        date_modified = (
                            last_modified.isoformat() if last_modified else ""
                        )
                        matching_files.append(
                            format_item(
                                file_name,
                                True,
                                f"/{bucket_name}/{key}",
                                False,
                                "file",
                                size,
                                date_modified,
                            )
                        )
                for common_prefix in response.get("CommonPrefixes", []):
                    folder_prefix = common_prefix.get("Prefix", "")
                    if search_text in folder_prefix.lower():
                        folder_name = folder_prefix.rstrip("/").split("/")[-1]
                        matching_folders.append(
                            format_item(
                                folder_name,
                                False,
                                f"/{bucket_name}/{folder_prefix}",
                                True,
                                "folder",
                            )
                        )
                cwd_name = prefix.split("/")[-1] if prefix else bucket_name
                cwd_path = f"/{bucket_name}/{prefix}".rstrip("/")
                if not cwd_path:
                    cwd_path = f"/{bucket_name}/"
                cwd = format_item(cwd_name, False, cwd_path, True, "folder")
                return json.dumps(
                    {"cwd": cwd, "files": matching_folders + matching_files}
                )
            except Exception as e:
                self.set_status(500)
                return json.dumps({"error": str(e)})
