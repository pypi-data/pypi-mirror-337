import json
import tornado
import tornado.web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.serverapp import ServerApp
from jupyter_server.utils import url_path_join
from .file_manager_handler import FileManagerHandler


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps({"data": "This is /jupyterlab-apibaker/get-example endpoint!"})
        )


def setup_handlers(web_app: ServerApp) -> None:
    host_pattern = ".*$"

    base_path = url_path_join(web_app.settings["base_url"], "jupyterlab-bxplorer-v2")
    handlers = [
        (url_path_join(base_path, "get-example"), RouteHandler),
        (url_path_join(base_path, "FileOperations"), FileManagerHandler),
    ]
    web_app.add_handlers(host_pattern, handlers)
