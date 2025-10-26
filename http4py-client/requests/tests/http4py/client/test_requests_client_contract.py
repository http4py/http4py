from __future__ import annotations

import importlib.util
from pathlib import Path

from http4py.client_requests import RequestsClient
from http4py.core import HttpHandler

# Import the shared contract from the core package
core_tests_path = Path(__file__).parent.parent.parent.parent.parent.parent / "http4py-core" / "tests"
contract_file_path = core_tests_path / "http4py" / "client" / "contract_http_client.py"
spec = importlib.util.spec_from_file_location("contract_http_client", contract_file_path)
contract_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract_module)

HttpClientContract = contract_module.HttpClientContract


class TestRequestsClientContract(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return RequestsClient()


class TestRequestsClientWithTimeout(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return RequestsClient(timeout=10.0)
