from __future__ import annotations

from http4py.client_requests import RequestsClient
from http4py.core import HttpHandler
from http4py.testing import HttpClientContract


class TestRequestsClientContract(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return RequestsClient(timeout=10.0)
