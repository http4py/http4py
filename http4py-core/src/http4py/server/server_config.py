from __future__ import annotations

from abc import ABC, abstractmethod

from http4py.core import HttpHandler
from http4py.server import Http4pyServer


class ServerConfig(ABC):
    @abstractmethod
    def serve(self, http: HttpHandler) -> Http4pyServer:
        pass
