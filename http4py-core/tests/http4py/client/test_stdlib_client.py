from __future__ import annotations

from http4py.client import StdLibClient
from http4py.core import HttpHandler
from http4py.testing import HttpClientContract


class TestStdLibClient(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return StdLibClient()
