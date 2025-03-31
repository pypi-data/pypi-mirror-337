import json
import tornado
import tornado.web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.serverapp import ServerApp
from jupyter_server.utils import url_path_join
from .file_manager_handler import FileManagerHandler

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

class RouteHandler(BaseHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    # @tornado.web.authenticated
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
