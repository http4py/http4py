#!/usr/bin/env python3
"""
Simple HTTP Client Example using http4py

Demonstrates the beautiful symmetry:
- Server: HttpHandler that processes requests
- Client: HttpHandler that makes HTTP calls
- Same interface, same composability!
"""

from http4py.client import stdlib_client
from http4py.core import Request, Response
from http4py.core.method import GET, POST


def main() -> None:
    print("=== http4py Client Examples ===\n")

    # Example 1: Simple GET request
    print("1. Simple GET request:")
    request = Request(GET, "https://httpbin.org/get")
    response = stdlib_client(request)
    print(f"Status: {response.status}")
    print(f"Body: {response.body.text[:100]}...")
    print()

    # Example 2: GET with query parameters
    print("2. GET with query parameters:")
    request = Request(GET, "https://httpbin.org/get?param1=value1&param2=value2")
    response = stdlib_client(request)
    print(f"Status: {response.status}")
    print(f"Response contains our params: {'param1' in response.body.text}")
    print()

    # Example 3: POST with JSON body
    print("3. POST with JSON body:")
    import json

    data = {"name": "Alice", "age": 30}
    request = (
        Request(POST, "https://httpbin.org/post").body_(json.dumps(data)).header_("Content-Type", "application/json")
    )
    response = stdlib_client(request)
    print(f"Status: {response.status}")
    print(f"Posted data echoed back: {'Alice' in response.body.text}")
    print()

    # Example 4: Client is just an HttpHandler - can be composed!
    print("4. Composable client (with logging):")

    def logging_client(request: Request) -> Response:
        print(f"  → Making {request.method.name} request to {request.uri}")
        response = stdlib_client(request)
        print(f"  ← Received {response.status.code} response")
        return response

    request = Request(GET, "https://httpbin.org/status/200")
    response = logging_client(request)
    print(f"Final status: {response.status}")
    print()

    # Example 5: Error handling (4xx/5xx responses)
    print("5. Error handling:")
    request = Request(GET, "https://httpbin.org/status/404")
    response = stdlib_client(request)
    print(f"404 Status: {response.status}")
    print(f"Is error response: {response.status.code >= 400}")
    print()

    print("=== All examples completed! ===")


if __name__ == "__main__":
    main()
