#!/usr/bin/env python3
"""
Simple HTTP Client Example using http4py

Demonstrates the beautiful symmetry:
- Server: HttpHandler that processes requests
- Client: HttpHandler that makes HTTP calls
- Same interface, same composability!

Shows both built-in Python client and optional Requests client.
"""

from http4py.client import StdLibClient
from http4py.core import Request, Response
from http4py.core.method import GET, POST

try:
    from http4py.client_requests import RequestsClient

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def main() -> None:
    print("=== http4py Client Examples ===\n")

    # Example 1: Simple GET request with stdlib client
    print("1. Simple GET request (Python stdlib client):")
    request = Request(GET, "https://httpbin.org/get")
    client = StdLibClient()
    response = client(request)
    print(f"Status: {response.status}")
    print(f"Body: {response.body.text[:100]}...")
    print()

    # Example 2: Same request with Requests client (if available)
    if HAS_REQUESTS:
        print("2. Same request with Requests client:")
        requests_client = RequestsClient()
        response = requests_client(request)
        print(f"Status: {response.status}")
        print(f"Body: {response.body.text[:100]}...")
        print()

    # Example 3: GET with query parameters
    print("3. GET with query parameters:")
    request = Request(GET, "https://httpbin.org/get?param1=value1&param2=value2")
    response = client(request)
    print(f"Status: {response.status}")
    print(f"Response contains our params: {'param1' in response.body.text}")
    print()

    # Example 4: POST with JSON body
    print("4. POST with JSON body:")
    import json

    data = {"name": "Alice", "age": 30}
    request = (
        Request(POST, "https://httpbin.org/post").body_(json.dumps(data)).header_("Content-Type", "application/json")
    )
    response = client(request)
    print(f"Status: {response.status}")
    print(f"Posted data echoed back: {'Alice' in response.body.text}")
    print()

    # Example 5: Client is just an HttpHandler - can be composed!
    print("5. Composable client (with logging):")

    def logging_client(request: Request) -> Response:
        print(f"  → Making {request.method.name} request to {request.uri}")
        response = client(request)
        print(f"  ← Received {response.status.code} response")
        return response

    request = Request(GET, "https://httpbin.org/status/200")
    response = logging_client(request)
    print(f"Final status: {response.status}")
    print()

    # Example 6: Error handling (4xx/5xx responses)
    print("6. Error handling:")
    request = Request(GET, "https://httpbin.org/status/404")
    response = client(request)
    print(f"404 Status: {response.status}")
    print(f"Is error response: {response.status.code >= 400}")
    print()

    # Example 7: Requests client with custom session (if available)
    if HAS_REQUESTS:
        print("7. Requests client with custom timeout:")
        custom_client = RequestsClient(timeout=5.0)
        request = Request(GET, "https://httpbin.org/delay/1")
        response = custom_client(request)
        print(f"Status: {response.status}")
        print("Response time handled gracefully")
        print()

    print("=== All examples completed! ===")
    if not HAS_REQUESTS:
        print("\nNote: Install http4py-client-requests for additional client features")


if __name__ == "__main__":
    main()
