from __future__ import annotations

from http4py.server import ServerConfig
from http4py.server import StdLibServer
from http4py.testing import HttpServerContract


class TestStdLibServerContract(HttpServerContract):
    def create_server_config(self, port: int) -> ServerConfig:
        return StdLibServer(port)
