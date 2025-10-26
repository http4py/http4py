from __future__ import annotations

import json
import threading
import time
from abc import ABC, abstractmethod

from http4py.core import HttpHandler, Request, Response
from http4py.core.method import GET, POST
from http4py.core.status import OK, NOT_FOUND
from http4py.server import StdLib


class HttpClientContract(ABC):
    """Abstract test contract for HTTP clients."""

    @abstractmethod
    def create_client(self) -> HttpHandler:
        """Create an instance of the HTTP client to test."""
        pass

    def test_simple_get_request(self) -> None:
        """Test basic GET request functionality."""

        def simple_handler(request: Request) -> Response:
            return Response(OK).body_("Hello from http4py server!").header_("Content-Type", "text/plain")

        server = StdLib(0).serve(simple_handler).start()
        port = server.port()

        server_thread = threading.Thread(target=server.block, daemon=True)
        server_thread.start()
        time.sleep(0.1)

        try:
            client = self.create_client()
            request = Request(GET, f"http://localhost:{port}/")
            response = client(request)

            assert response.status == OK
            assert response.body.text == "Hello from http4py server!"
            assert response.headers["Content-Type"] == "text/plain"

        finally:
            server.stop()

    def test_post_with_simple_body(self) -> None:
        """Test POST request with simple text body."""

        def echo_handler(request: Request) -> Response:
            if request.method.name == "POST":
                # Echo back just the method and a simple confirmation
                return Response(OK).body_("POST received").header_("Content-Type", "text/plain")
            return Response(NOT_FOUND).body_("Not found")

        server = StdLib(0).serve(echo_handler).start()
        port = server.port()

        server_thread = threading.Thread(target=server.block, daemon=True)
        server_thread.start()
        time.sleep(0.2)  # Give more time for server to start

        try:
            client = self.create_client()
            request = (
                Request(POST, f"http://localhost:{port}/api/users")
                .body_("test data")
                .header_("Content-Type", "text/plain")
            )
            response = client(request)

            assert response.status == OK
            assert response.body.text == "POST received"
            assert response.headers["Content-Type"] == "text/plain"

        finally:
            server.stop()

    def test_error_handling(self) -> None:
        """Test handling of HTTP error responses."""

        def error_handler(request: Request) -> Response:
            return Response(NOT_FOUND).body_("Resource not found").header_("Content-Type", "text/plain")

        server = StdLib(0).serve(error_handler).start()
        port = server.port()

        server_thread = threading.Thread(target=server.block, daemon=True)
        server_thread.start()
        time.sleep(0.1)

        try:
            client = self.create_client()
            request = Request(GET, f"http://localhost:{port}/nonexistent")
            response = client(request)

            assert response.status == NOT_FOUND
            assert response.body.text == "Resource not found"

        finally:
            server.stop()

    def test_custom_headers(self) -> None:
        """Test sending custom headers."""

        def header_echo_handler(request: Request) -> Response:
            auth_header = request.headers.get("Authorization", "none")
            custom_header = request.headers.get("X-Custom-Header", "none")
            response_body = f"auth={auth_header},custom={custom_header}"
            return Response(OK).body_(response_body).header_("Content-Type", "text/plain")

        server = StdLib(0).serve(header_echo_handler).start()
        port = server.port()

        server_thread = threading.Thread(target=server.block, daemon=True)
        server_thread.start()
        time.sleep(0.1)

        try:
            client = self.create_client()
            request = (
                Request(GET, f"http://localhost:{port}/headers")
                .header_("Authorization", "Bearer token123")
                .header_("X-Custom-Header", "test-value")
            )
            response = client(request)

            assert response.status == OK
            assert "auth=Bearer token123" in response.body.text
            assert "custom=test-value" in response.body.text

        finally:
            server.stop()
