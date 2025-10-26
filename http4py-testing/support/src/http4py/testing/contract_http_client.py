from __future__ import annotations

from abc import ABC, abstractmethod

from http4py.core import HttpHandler, Request
from http4py.core.method import GET, POST
from http4py.core.status import OK, NOT_FOUND


class HttpClientContract(ABC):
    """Abstract test contract for HTTP clients."""

    @abstractmethod
    def create_client(self) -> HttpHandler:
        """Create an instance of the HTTP client to test."""
        pass

    def test_simple_get_request(self, test_server: str) -> None:
        """Test basic GET request functionality."""
        client = self.create_client()
        request = Request(GET, f"{test_server}/")
        response = client(request)

        assert response.status == OK
        assert response.body.text == "Hello from http4py server!"
        assert response.headers["Content-Type"] == "text/plain"

    def test_post_with_simple_body(self, test_server: str) -> None:
        """Test POST request with simple text body."""
        client = self.create_client()
        request = (
            Request(POST, f"{test_server}/api/users")
            .body_("test data")
            .header_("Content-Type", "text/plain")
        )
        response = client(request)

        assert response.status == OK, f"Expected 200 OK, got {response.status} ({response.status.code}). Body: {response.body.text!r}"
        assert response.body.text == "POST received", f"Expected 'POST received', got {response.body.text!r}"
        assert response.headers[
                   "Content-Type"] == "text/plain", f"Expected text/plain content-type, got {response.headers.get('Content-Type')}"

    def test_error_handling(self, test_server: str) -> None:
        """Test handling of HTTP error responses."""
        client = self.create_client()
        request = Request(GET, f"{test_server}/nonexistent")
        response = client(request)

        assert response.status == NOT_FOUND

    def test_custom_headers(self, test_server: str) -> None:
        """Test sending custom headers."""
        client = self.create_client()
        request = (
            Request(GET, f"{test_server}/headers")
            .header_("Authorization", "Bearer token123")
            .header_("X-Custom-Header", "test-value")
        )
        response = client(request)

        assert response.status == OK
        assert "auth=Bearer token123" in response.body.text
        assert "custom=test-value" in response.body.text
