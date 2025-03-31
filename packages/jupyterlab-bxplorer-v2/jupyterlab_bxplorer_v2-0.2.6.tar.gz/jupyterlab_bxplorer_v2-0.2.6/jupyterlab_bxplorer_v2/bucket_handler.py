import json
import logging
import tornado
import tornado.web
import json
import yaml
import asyncio
from jupyter_server.base.handlers import APIHandler


import json
import asyncio
import tornado.web
import tornado.httpclient
import yaml
import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# ---------------------------
# Configuración de SQLAlchemy
# ---------------------------

Base = declarative_base()


class Cache(Base):
    __tablename__ = "cache"
    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


# Creamos el engine de SQLite y el sessionmaker.
engine = create_engine(
    "sqlite:///cache.db", echo=False, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)

# Crear la tabla (si no existe)
Base.metadata.create_all(bind=engine)

# Definimos un TTL (en segundos) para la caché, por ejemplo 1 hora (3600 segundos)
CACHE_TTL = 3600

# ---------------------------
# Handler de Tornado
# ---------------------------


class BucketHandler(APIHandler):
    async def get(self):
        session = SessionLocal()
        try:
            # Consultamos si existe una entrada en caché para la clave "buckets"
            cache_entry = session.query(Cache).filter(Cache.key == "public_buckets").first()
            now = datetime.datetime.utcnow()
            if (
                cache_entry
                and (now - cache_entry.timestamp).total_seconds() < CACHE_TTL
            ):
                # Si la entrada existe y es reciente, devolvemos el caché
                self.set_header("Content-Type", "application/json")
                self.write(cache_entry.value)
                return
        except Exception as e:
            self.application.settings.get("logger", print)(
                f"Error al acceder a cache: {e}"
            )

        # Si no hay caché o ha caducado, procedemos a obtener los datos
        http_client = tornado.httpclient.AsyncHTTPClient()
        datasets_url = (
            "https://api.github.com/repos/awslabs/open-data-registry/contents/datasets"
        )

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

        logger.error(f"Resultados finales: {final_results}")
        logger.error(f"Tipo Resultados finales: {type(final_results)}")

        flattened = [obj for sublist in final_results for obj in sublist]

        result_json = json.dumps({"data": flattened}, indent=2)
        self.set_header("Content-Type", "application/json")
        self.write(result_json)

        # Guardamos/actualizamos el resultado en caché
        try:
            if cache_entry:
                cache_entry.value = result_json
                cache_entry.timestamp = datetime.datetime.utcnow()
            else:
                cache_entry = Cache(
                    key="buckets",
                    value=result_json,
                    timestamp=datetime.datetime.utcnow(),
                )
                session.add(cache_entry)
            session.commit()
        except Exception as e:
            self.application.settings.get("logger", print)(
                f"Error al guardar en cache: {e}"
            )
        finally:
            session.close()

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
            file_obj = {
                "name": bucket_name,
                "isFile": False,
                "path": f"/{bucket_name}/",
                "hasChild": True,
                "type": "folder",
                "size": 0,
                "dateModified": "",
            }
            files_list.append(file_obj)

        return files_list
