"""Lightweight web server utilities for project GUIs."""

import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROUTES = {}


def route(path_or_function):
    """Register an HTTP route handler."""
    if callable(path_or_function):
        ROUTES[path_or_function.__name__] = path_or_function
        return path_or_function

    path = str(path_or_function).lstrip("/")

    def register(function):
        ROUTES[path] = function
        return function

    return register


def _normalize_gui_path(gui_folder):
    return os.path.abspath(gui_folder.rstrip("/"))


def _run_initializers(initializers):
    for initialize in initializers:
        if callable(initialize):
            initialize()


def _safe_header_value(value):
    return str(value).replace("\r", "").replace("\n", "")


def start(port, default_server, gui_folder, *initializers, host="127.0.0.1"):
    """Start a small local HTTP server for the GUI."""
    _run_initializers(initializers)
    gui_root = _normalize_gui_path(gui_folder)

    class GUIHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self._handle_request("GET")

        def do_POST(self):
            self._handle_request("POST")

        def _handle_request(self, method):
            parsed = urlparse(self.path)
            route_path = parsed.path.lstrip("/")

            if route_path in ROUTES:
                payload = self._payload(method, parsed.query)
                response = self._invoke(ROUTES[route_path], payload)
                return self._write_route_response(response)

            static_path = "index.html" if route_path == "" else route_path
            local_file = os.path.abspath(os.path.join(gui_root, static_path))
            if local_file.startswith(gui_root + os.sep) and os.path.isfile(local_file):
                return self._write_file(local_file)

            target = default_server.rstrip("/")
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", _safe_header_value(target))
            self.end_headers()

        def _payload(self, method, query):
            if method == "POST":
                body_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(body_length) if body_length else b"{}"
                try:
                    return json.loads(body)
                except json.JSONDecodeError:
                    return {}

            args = parse_qs(query, keep_blank_values=True)
            return {k: v for k, v in args.items()}

        def _invoke(self, handler, payload):
            if isinstance(payload, list):
                return handler(*payload)
            if isinstance(payload, dict):
                try:
                    return handler(**payload)
                except TypeError:
                    return handler(*payload.values())
            return handler()

        def _write_route_response(self, response):
            if isinstance(response, (dict, list, int, float, bool)) or response is None:
                body = json.dumps(response).encode("utf-8")
                content_type = "application/json"
            else:
                body = str(response).encode("utf-8")
                content_type = "text/plain; charset=utf-8"

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_file(self, path):
            with open(path, "rb") as file_obj:
                data = file_obj.read()

            content_type, _ = mimetypes.guess_type(path)
            self.send_response(HTTPStatus.OK)
            self.send_header(
                "Content-Type",
                _safe_header_value(content_type or "application/octet-stream"),
            )
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *_args):
            return

    server = ThreadingHTTPServer((host, port), GUIHandler)
    print(f"Starting Hog GUI at http://{host}:{port}")
    print(f"If local gui files are missing, requests redirect to {default_server}.")
    server.serve_forever()
    return server
