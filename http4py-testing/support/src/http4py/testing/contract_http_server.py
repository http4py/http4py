from __future__ import annotations

import socket
from abc import ABC, abstractmethod

from http4py.core import Request, Response
from http4py.core.status import OK
from http4py.server import Http4pyServer, ServerConfig


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        return s.getsockname()[1]


class HttpServerContract(ABC):
    @abstractmethod
    def create_server_config(self, port: int) -> ServerConfig:
        pass

    def test_server_creation(self) -> None:
        def handler(request: Request) -> Response:
            return Response(OK).body_("Hello World")

        port = get_free_port()
        config = self.create_server_config(port)
        server = config.serve(handler)
        assert server.port() == port

    def test_server_start_returns_same_instance(self) -> None:
        def handler(request: Request) -> Response:
            return Response(OK).body_("Hello World")

        port = get_free_port()
        config = self.create_server_config(port)
        server = config.serve(handler)

        started_server = server.start()
        assert started_server is server
        assert started_server.port() == port
