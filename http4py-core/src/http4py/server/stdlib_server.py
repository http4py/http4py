from __future__ import annotations

from http.server import HTTPServer
from typing import Any

from http4py.core import HttpHandler

from .request_handler import Http4pyRequestHandler
from .server import Http4pyServer
from .server_config import ServerConfig


class StdLib(ServerConfig):
    def __init__(self, port: int = 8080):
        self._port = port

    def serve(self, http: HttpHandler) -> Http4pyServer:
        class _StdLibServer(Http4pyServer):
            def __init__(self, host: str, port: int, http_handler: HttpHandler):
                self._host = host
                self._port = port
                self._http_handler = http_handler
                self._server: HTTPServer | None = None

            def start(self) -> Http4pyServer:
                if self._server is not None:
                    return self

                def handler_factory(*args: Any, **kwargs: Any) -> Http4pyRequestHandler:
                    return Http4pyRequestHandler(self._http_handler, *args, **kwargs)

                self._server = HTTPServer((self._host, self._port), handler_factory)
                return self

            def stop(self) -> Http4pyServer:
                if self._server is not None:
                    self._server.shutdown()
                    self._server.server_close()
                    self._server = None
                return self

            def block(self) -> None:
                if self._server is not None:
                    self._server.serve_forever()

            def port(self) -> int:
                if self._server is not None:
                    return self._server.server_address[1]
                return self._port

        return _StdLibServer("localhost", self._port, http)
