from __future__ import annotations

from http4py.client import PythonClient
from http4py.core import HttpHandler

from .contract_http_client import HttpClientContract


class TestPythonClient(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return PythonClient()
