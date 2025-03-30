import boto3
import functools
import json
import logging
import os
import tornado
import tornado.web

from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError
from jupyter_server.base.handlers import APIHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("nose").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


@functools.lru_cache()
def _get_signed_s3_client():
    session = boto3.Session()
    s3 = session.client("s3")  # type: ignore
    return s3


@functools.lru_cache()
def _get_unsigned_s3_client():
    s3 = boto3.client(
        "s3",
        region_name="us-east-1",
        config=Config(max_pool_connections=50, signature_version=UNSIGNED),
    )
    return s3


class FileManagerHandler(APIHandler):
    def set_default_headers(self):
        self.set_header(
            "Access-Control-Allow-Origin", "*"
        )  # Cambia "*" por el origen específico si es necesario
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self):
        self.set_status(204)
        self.finish()

    @tornado.web.authenticated
    def get(self):
        logger.error("GET request")
        action = self.get_argument("action", "").lower()
        path = self.get_argument("path", "")
        if not action or not path:
            self.set_status(400)
            self.write("Parámetros requeridos: action y path")
            return
        full_path = os.path.join(BASE_DIR, path.lstrip("/"))

        if action == "download":
            self.download_item(full_path)
        else:
            self.set_status(400)
            self.write("Acción no soportada")

    @tornado.web.authenticated
    def post(self):
        logger.error("POST request")
        logger.error(f"Request Body: {self.request.body}")
        try:
            BASE_DIR = os.path.expanduser(
                "/Users/luisleon/Projects/Navteca/OSS/jupyterlab-new-version-extensions/jupyterlab-bxplorer43/Downloads"
            )
            # Obtener cliente de S3
            if self.request.body:
                content_type = self.request.headers.get("Content-Type", "")
                if "application/x-www-form-urlencoded" in content_type:
                    # Extraemos el parámetro 'downloadInput' del formulario
                    download_input = self.get_body_argument("downloadInput", None)
                    if download_input is None:
                        raise Exception("No se encontró el parámetro downloadInput")
                    data = json.loads(download_input)
                else:
                    data = json.loads(self.request.body)

                action = data.get("action", "").lower()
                path = data.get("path", "")
                client_type = data.get("client_type", "private")
            else:
                # Si no hay body, se obtienen los parámetros de la URL
                action = self.get_argument("action", "").lower()
                path = self.get_argument("path", "")
                client_type = self.get_argument("client_type", "private")

            full_path = os.path.join(BASE_DIR, path.lstrip("/"))

            logger.error(f"Data => {data}")
            logger.error(f"Client Type => {client_type}")
            s3 = (
                _get_unsigned_s3_client()
                if client_type == "public"
                else _get_signed_s3_client()
            )

            action = data.get("action")

            logger.info(f"Action => {action}")
            if action == "read":
                self.read_files(data, s3)
            elif action == "download":
                self.download_file(data, s3)
            elif action == "details":
                self.get_file_details(data, s3)
            elif action == "search":
                self.search_files(data, s3)
            elif action == "getImage":
                self.get_image(data, s3)
            else:
                self.set_status(400)
                self.write({"error": "Acción no soportada"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

    def read_files(self, data, s3):
        try:
            logger.error(f"Data => {data}")
            raw_path = data.get("path", "").strip()
            # Eliminamos barras iniciales para obtener una ruta limpia
            sanitized_path = raw_path.lstrip("/")
            logger.error(f"Ruta sanitizada: {sanitized_path}")

            # Si no se especifica ruta, listamos los buckets
            if not sanitized_path:
                response = s3.list_buckets()
                buckets = [
                    {
                        "name": bucket.get("Name"),
                        "isFile": False,
                        "path": f"/{bucket.get('Name')}/",
                        "hasChild": True,
                        "type": "folder",
                    }
                    for bucket in response.get("Buckets", [])
                ]
                cwd = {
                    "name": "Root",
                    "isFile": False,
                    "path": "/",
                    "hasChild": bool(buckets),
                    "type": "folder",
                }
                self.write({"cwd": cwd, "files": buckets})
                return

            # Separar el nombre del bucket y el prefijo dentro del bucket
            path_parts = sanitized_path.split("/", 1)
            bucket_name = path_parts[0]
            prefix_path = path_parts[1] if len(path_parts) > 1 else ""

            # Verificar permisos sobre el bucket
            try:
                s3.head_bucket(Bucket=bucket_name)
            except ClientError as e:
                self.set_status(403)
                self.write({"error": "No tienes permisos para acceder a este bucket."})
                return

            logger.error(f"Bucket: {bucket_name}, Prefix: {prefix_path}")

            # Manejo de paginación y listado de archivos y carpetas
            all_files = []
            all_folders = []
            continuation_token = None
            while True:
                list_params = {
                    "Bucket": bucket_name,
                    "Prefix": prefix_path,
                    "Delimiter": "/",
                }
                if continuation_token:
                    list_params["ContinuationToken"] = continuation_token

                response = s3.list_objects_v2(**list_params)

                # Procesar archivos (evitando que se incluya el objeto que representa la carpeta)
                files = [
                    {
                        "name": obj["Key"].split("/")[-1],
                        "size": obj.get("Size", 0),
                        "isFile": True,
                        "path": f"/{bucket_name}/{obj['Key']}",
                        "hasChild": False,
                        "type": "file",
                    }
                    for obj in response.get("Contents", [])
                    if obj["Key"]
                    != prefix_path  # Se omite el objeto que define la carpeta
                ]
                all_files.extend(files)

                # Procesar carpetas
                folders = [
                    {
                        "name": folder["Prefix"].rstrip("/").split("/")[-1],
                        "isFile": False,
                        "path": f"/{bucket_name}/{folder['Prefix']}",
                        "hasChild": True,
                        "type": "folder",
                    }
                    for folder in response.get("CommonPrefixes", [])
                ]
                all_folders.extend(folders)

                # Verificar si la respuesta está truncada (más páginas)
                if response.get("IsTruncated"):
                    continuation_token = response.get("NextContinuationToken")
                else:
                    break

            # Construir el directorio actual (cwd)
            cwd_name = prefix_path.split("/")[-1] if prefix_path else bucket_name
            cwd_path = f"/{bucket_name}/{prefix_path}".rstrip("/")
            if not cwd_path:
                cwd_path = f"/{bucket_name}/"
            cwd = {
                "name": cwd_name,
                "isFile": False,
                "path": cwd_path,
                "hasChild": True,
                "type": "folder",
            }

            # Devolver la respuesta combinando carpetas y archivos
            self.write({"cwd": cwd, "files": all_folders + all_files})
        except Exception as e:
            logger.exception("Error en read_files")
            self.set_status(500)
            self.write({"error": str(e)})

    def download_file(self, data, s3):
        try:
            LOCAL_SAVE_DIR = "tmp"
            if data.get("downloadsFolder"):
                LOCAL_SAVE_DIR = data.get("downloadsFolder")

            logger.error(f"LOCAL_SAVE_DIR: {LOCAL_SAVE_DIR}")
            logger.error(f"Download Request Data: {data}")
            # Si se envía información del archivo en "data", se utiliza esa ruta completa.
            if data.get("data") and len(data.get("data")) > 0:
                file_full_path = data["data"][0].get("path")
            else:
                # Si no, se arma la ruta combinando 'path' y 'names'
                file_full_path = os.path.join(data.get("path"), data.get("names")[0])

            # Limpiar la ruta y separar en bucket y key
            file_path = file_full_path.strip("/")
            parts = file_path.split("/", 1)
            if len(parts) < 2:
                raise Exception(
                    "La ruta del archivo no tiene el formato esperado: 'bucket/key'"
                )
            bucket_name, key = parts

            # Obtener el objeto desde AWS S3.
            file_obj = s3.get_object(Bucket=bucket_name, Key=key)
            file_content = file_obj["Body"].read()

            # Crear el directorio local si no existe.
            os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)
            # Definir la ruta completa del archivo a guardar.
            local_file_path = os.path.join(LOCAL_SAVE_DIR, os.path.basename(key))

            # Guardar el contenido del archivo en el directorio predefinido.
            with open(local_file_path, "wb") as f:
                f.write(file_content)

            logger.error(f"Archivo descargado y guardado en: {local_file_path}")
            # Responder con un JSON indicando éxito y la ruta donde se guardó el archivo.
            self.write(json.dumps({"success": True, "file_saved": local_file_path}))
        except ClientError as e:
            self.set_status(403)
            self.write(
                json.dumps({"error": "No tienes permisos para descargar este archivo."})
            )
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

    def get_file_details(self, data, s3):
        try:
            logger.info(f"Details Request Data: {data}")

            items = data.get("data", [])
            if not items:
                self.set_status(400)
                self.write({"error": "Parámetro 'data' es requerido."})
                return

            details = []

            for item in items:
                full_path = item.get("path", "").strip("/")
                if not full_path:
                    continue

                # Separar en bucket y clave (object_key)
                path_parts = full_path.split("/", 1)
                bucket_name = path_parts[0]
                object_key = path_parts[1] if len(path_parts) > 1 else ""

                # Validar permisos sobre el bucket
                try:
                    s3.head_bucket(Bucket=bucket_name)
                except ClientError:
                    self.set_status(403)
                    self.write(
                        {
                            "error": f"No tienes permisos para acceder al bucket {bucket_name}."
                        }
                    )
                    return

                # Determinar si es carpeta (no hay object_key o termina en '/')
                if not object_key or object_key.endswith("/"):
                    # Es carpeta
                    # Aseguramos que el path final termine con '/'
                    folder_path = (
                        object_key
                        if object_key.endswith("/")
                        else (object_key + "/") if object_key else ""
                    )
                    folder_detail = {
                        "name": item.get("name"),
                        "isFile": False,
                        "type": "folder",
                        "path": f"/{bucket_name}/{folder_path}",
                        "size": 0,
                        "modified": "",  # Cadena vacía para evitar "null"
                        "hasChild": True,
                        # filterPath => carpeta padre (ej. "/bucket_name" si no hay subcarpetas)
                        "location": (
                            f"/{bucket_name}/"
                            if not folder_path
                            else f"/{bucket_name}/"
                            + "/".join(folder_path.strip("/").split("/")[:-1])
                        ),
                    }
                    details.append(folder_detail)
                    continue

                # Caso: Se asume archivo. Intentamos head_object
                try:
                    response = s3.head_object(Bucket=bucket_name, Key=object_key)
                    last_modified = response.get("LastModified")
                    date_mod_str = last_modified.isoformat() if last_modified else ""

                    # Construir filterPath (la carpeta padre)
                    if "/" in object_key:
                        parent_path = "/".join(object_key.split("/")[:-1])
                        filter_path = f"/{bucket_name}/{parent_path}"
                    else:
                        filter_path = f"/{bucket_name}/"

                    file_detail = {
                        "name": item.get("name"),
                        "isFile": True,
                        "type": "file",
                        "path": f"/{bucket_name}/{object_key}",
                        "size": response.get("ContentLength", 0),
                        "modified": date_mod_str,
                        "hasChild": False,
                        "location": filter_path,
                    }
                    details.append(file_detail)

                except ClientError as e:
                    # Si el error es 404 o NoSuchKey, tratamos el item como carpeta "virtual"
                    error_code = e.response["Error"]["Code"]
                    if error_code in ["404", "NoSuchKey"]:
                        folder_path = object_key + "/"
                        folder_detail = {
                            "name": item.get("name"),
                            "isFile": False,
                            "type": "folder",
                            "path": f"/{bucket_name}/{folder_path}",
                            "size": 0,
                            "modified": "",
                            "hasChild": True,
                            "location": (
                                f"/{bucket_name}/"
                                + "/".join(object_key.split("/")[:-1])
                                if "/" in object_key
                                else f"/{bucket_name}/"
                            ),
                        }
                        details.append(folder_detail)
                    else:
                        logger.error(
                            f"Error obteniendo detalles de {object_key}: {str(e)}"
                        )
                        self.set_status(403)
                        self.write(
                            {
                                "error": f"No tienes permisos para acceder al objeto {object_key}."
                            }
                        )
                        return

            # Enviar respuesta con la estructura que Syncfusion espera
            self.write({"details": details[0]})

        except Exception as e:
            logger.error(f"Unexpected error in get_file_details: {str(e)}")
            self.set_status(500)
            self.write({"error": "Error interno del servidor."})

    def search_files(self, data, s3):
        try:
            search_text = (
                data.get("searchString", "").lower().replace("*", "")
            )  # Remueve '*'
            path = data.get("path", "").strip("/")

            if not search_text:
                self.set_status(400)
                self.write({"error": "Parámetro 'searchString' es requerido"})
                return

            # ✅ Si la búsqueda se hace en la raíz ("/"), listar todos los buckets
            if path == "":
                response = s3.list_buckets()
                matching_buckets = [
                    {
                        "name": bucket["Name"],
                        "isFile": False,
                        "path": f"/{bucket['Name']}/",
                        "hasChild": True,
                        "type": "folder",
                    }
                    for bucket in response["Buckets"]
                    if search_text in bucket["Name"].lower()
                ]

                cwd = {
                    "name": "Root",
                    "isFile": False,
                    "path": "/",
                    "hasChild": bool(matching_buckets),
                    "type": "folder",
                }
                self.write({"cwd": cwd, "files": matching_buckets})
                return

            # ✅ Extraer bucket y prefijo
            path_parts = path.split("/", 1)
            bucket_name = path_parts[0]
            prefix_path = path_parts[1] if len(path_parts) > 1 else ""

            # Verificar permisos sobre el bucket
            try:
                s3.head_bucket(Bucket=bucket_name)
            except ClientError:
                self.set_status(403)
                self.write({"error": "No tienes permisos para acceder a este bucket."})
                return

            logger.error(
                f"Bucket: {bucket_name}, Prefix: {prefix_path}, Searched Text: {search_text}"
            )
            # Buscar archivos y carpetas en el bucket
            response = s3.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix_path, Delimiter="/"
            )
            logger.error(f"Response.Contents: {response.get("Contents", [])}")
            logger.error(
                f"Response.CommonPrefixes: {response.get("CommonPrefixes", [])}"
            )
            matching_files = [
                {
                    "name": obj["Key"].split("/")[-1],
                    "size": obj.get("Size", 0),
                    "isFile": True,
                    "path": f"/{bucket_name}/{obj['Key']}",
                    "hasChild": False,
                    "type": "file",
                }
                for obj in response.get("Contents", [])
                if search_text in obj["Key"].lower()
            ]
            logger.error(f"Matching Files: {matching_files}")

            matching_folders = [
                {
                    "name": (
                        folder["Prefix"].split("/")[-2]
                        if folder["Prefix"].endswith("/")
                        else folder["Prefix"].split("/")[-1]
                    ),
                    "isFile": False,
                    "path": f"/{bucket_name}/{folder['Prefix']}",
                    "hasChild": True,
                    "type": "folder",
                }
                for folder in response.get("CommonPrefixes", [])
                if search_text in folder["Prefix"].lower()
            ]
            logger.error(f"Matching Folders: {matching_folders}")

            # Definir el nodo padre (cwd)
            cwd = {
                "name": prefix_path.split("/")[-1] if prefix_path else bucket_name,
                "isFile": False,
                "path": f"/{bucket_name}/{prefix_path}",
                "hasChild": True,
                "type": "folder",
            }

            # Enviar la respuesta en el formato esperado
            self.write({"cwd": cwd, "files": matching_folders + matching_files})

        except ClientError as e:
            self.set_status(500)
            self.write({"error": str(e)})

    def list_public_buckets(self, data, s3):
        try:
            logger.error(f"list_public_buckets => ")
            # Crear el cliente sin firma
            s3_client = _get_unsigned_s3_client()
            logger.error(f"s3_client = _get_unsigned_s3_client() => ")
            response = s3_client.list_buckets()
            logger.error(f"response = s3_client.list_buckets() => ")
            # Procesar cada bucket para formatear la respuesta acorde al FileManager
            buckets = response.get("Buckets", [])
            logger.error(f"buckets = response.get(Buckets, []) => ")
            buckets_list = [
                {
                    "name": bucket["Name"],
                    "isFile": False,
                    "path": f"/{bucket['Name']}/",
                    "size": 0,
                    "dateModified": "",
                    "hasChild": True,
                    "type": "folder",
                    "filterPath": "/",  # Asumiendo que la raíz es la ubicación padre
                }
                for bucket in buckets
            ]

            # Definir el directorio actual (cwd) como la raíz
            cwd = {
                "name": "Root",
                "isFile": False,
                "path": "/",
                "size": 0,
                "dateModified": "",
                "hasChild": bool(buckets),
                "type": "folder",
                "filterPath": "/",
            }

            return {"cwd": cwd, "files": buckets_list}
        except Exception as e:
            logger.exception("Error listando buckets públicos")
            logger.error(f"Unexpected error in get_file_details: {str(e)}")
            raise e
