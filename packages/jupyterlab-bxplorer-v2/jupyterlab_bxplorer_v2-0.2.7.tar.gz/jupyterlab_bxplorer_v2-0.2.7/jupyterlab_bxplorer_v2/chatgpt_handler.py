import os
import json
import datetime
import asyncio

import tornado.web
import tornado.ioloop
import tornado.httpclient

import boto3
from botocore.exceptions import ClientError
from botocore import UNSIGNED
from botocore.config import Config

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------------
# Configuración de SQLAlchemy para el caché de buckets públicos
# -----------------------------------------------------------
Base = declarative_base()

class Cache(Base):
    __tablename__ = "cache"
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

engine = create_engine('sqlite:///cache.db', echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# TTL para el caché (por defecto 5 minutos)
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
# URL para descargar la lista de buckets públicos (configurable vía variable de entorno)
PUBLIC_BUCKETS_URL = os.getenv("PUBLIC_BUCKETS_URL", "https://example.com/public_buckets.json")
# Directorio local para guardar descargas
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR", "tmp")

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
        return boto3.client("s3")

def format_item(name, is_file, path, has_child, item_type, size=0, date_modified=""):
    """
    Formatea un item (archivo o carpeta) según lo espera FileManager.
    """
    return {
        "name": name,
        "isFile": is_file,
        "path": path,
        "hasChild": has_child,
        "type": item_type,
        "size": size,
        "dateModified": date_modified,
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
        list_params = {
            "Bucket": bucket_name,
            "Prefix": prefix,
            "Delimiter": "/"
        }
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
            all_files.append(format_item(file_name, True, f"/{bucket_name}/{key}", False, "file", size, date_modified))

        # Procesar carpetas
        for common_prefix in response.get("CommonPrefixes", []):
            folder_prefix = common_prefix.get("Prefix", "")
            folder_name = folder_prefix.rstrip("/").split("/")[-1]
            all_folders.append(format_item(folder_name, False, f"/{bucket_name}/{folder_prefix}", True, "folder"))

        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    return all_folders + all_files

# -----------------------------------------------------------
# Handler Unificado para FileManager (operaciones: read, download, details)
# -----------------------------------------------------------
class FileManagerHandler(tornado.web.RequestHandler):
    async def post(self):
        # Parseamos la solicitud JSON
        try:
            data = json.loads(self.request.body) if self.request.body else {}
        except Exception as e:
            self.set_status(400)
            self.write({"error": "Error en el parseo del JSON: " + str(e)})
            return

        action = data.get("action", "").lower()
        path = data.get("path", "").strip()   # Ej: "/bucket_name/optional_prefix"
        # client_type determina si se opera sobre buckets "private" o "public"
        client_type = data.get("client_type", "private").lower()
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
        else:
            self.set_status(400)
            self.write({"error": "Acción no soportada"})

    def _list_private_buckets(self, s3_client):
        """
        Listado de buckets privados usando list_buckets.
        """
        try:
            response = s3_client.list_buckets()
            buckets = []
            for bucket in response.get("Buckets", []):
                name = bucket.get("Name")
                buckets.append(format_item(name, False, f"/{name}/", True, "folder"))
            cwd = format_item("Root", False, "/", True, "folder")
            return json.dumps({"cwd": cwd, "files": buckets})
        except ClientError:
            self.set_status(403)
            return json.dumps({"error": "No tienes permisos para acceder a los buckets privados."})
        except Exception as e:
            self.set_status(500)
            return json.dumps({"error": str(e)})

    async def _list_public_buckets(self):
        """
        Obtiene la lista de buckets públicos a partir de un archivo JSON (descargado y cacheado).
        """
        session = SessionLocal()
        cache_key = "public_buckets"
        try:
            cache_entry = session.query(Cache).filter(Cache.key == cache_key).first()
            now = datetime.datetime.utcnow()
            if cache_entry and (now - cache_entry.timestamp).total_seconds() < CACHE_TTL:
                return cache_entry.value
        except Exception as e:
            print(f"Error al acceder al caché: {e}")

        # No hay datos en caché o han expirado; se descarga el JSON
        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(PUBLIC_BUCKETS_URL)
            buckets_data = json.loads(response.body.decode())
            buckets = []
            # Se asume que buckets_data es una lista de objetos con al menos 'name'
            for item in buckets_data:
                name = item.get("name")
                if name:
                    buckets.append(format_item(name, False, f"/{name}/", True, "folder"))
            cwd = format_item("Root", False, "/", True, "folder")
            result = json.dumps({"cwd": cwd, "files": buckets})
            try:
                if cache_entry:
                    cache_entry.value = result
                    cache_entry.timestamp = datetime.datetime.utcnow()
                else:
                    cache_entry = Cache(key=cache_key, value=result, timestamp=datetime.datetime.utcnow())
                    session.add(cache_entry)
                session.commit()
            except Exception as e:
                print(f"Error guardando en caché: {e}")
            finally:
                session.close()
            return result
        except Exception as e:
            self.set_status(500)
            return json.dumps({"error": "Error al descargar buckets públicos: " + str(e)})

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
                return json.dumps({"error": f"No tienes permisos para acceder al bucket {bucket_name}."})
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
                file_full_path = os.path.join(data.get("path", ""), data.get("names", [""])[0])
            file_path = file_full_path.strip("/")
            parts = file_path.split("/", 1)
            if len(parts) < 2:
                self.set_status(400)
                self.write(json.dumps({"error": "La ruta del archivo debe tener el formato 'bucket/key'"}))
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
            self.write(json.dumps({"error": "No tienes permisos para descargar este archivo."}))
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
                    self.write(json.dumps({"error": f"No tienes permisos para acceder al bucket {bucket_name}."}))
                    return
                if not object_key or object_key.endswith("/"):
                    folder_detail = format_item(item.get("name"), False, f"/{bucket_name}/{object_key}", True, "folder")
                    details.append(folder_detail)
                else:
                    try:
                        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
                        last_modified = response.get("LastModified")
                        date_mod_str = last_modified.isoformat() if last_modified else ""
                        file_detail = format_item(item.get("name"), True, f"/{bucket_name}/{object_key}", False, "file", response.get("ContentLength", 0), date_mod_str)
                        details.append(file_detail)
                    except ClientError as e:
                        code = e.response["Error"]["Code"]
                        if code in ["404", "NoSuchKey"]:
                            folder_detail = format_item(item.get("name"), False, f"/{bucket_name}/{object_key}/", True, "folder")
                            details.append(folder_detail)
                        else:
                            self.set_status(403)
                            self.write(json.dumps({"error": f"No tienes permisos para acceder al objeto {object_key}."}))
                            return
            self.write(json.dumps({"details": details[0] if details else {}}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": "Error interno del servidor: " + str(e)}))

# -----------------------------------------------------------
# Función de creación y ejecución de la aplicación
# -----------------------------------------------------------
def make_app():
    return tornado.web.Application([
        (r"/FileOperations", FileManagerHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    port = int(os.getenv("PORT", "8888"))
    app.listen(port)
    print(f"Servidor corriendo en http://localhost:{port}")
    tornado.ioloop.IOLoop.current().start()
