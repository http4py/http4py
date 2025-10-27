# http4py-client-requests

HTTP client implementation using the popular requests library.

## Overview

This package provides an HTTP client that implements the `HttpHandler` interface using the requests library as the underlying HTTP transport.

### Components
- **RequestsClient** - HTTP client using requests library
- **Contract Tests** - Ensures compliance with http4py client behavior

## Features

- **Requests Integration** - Leverages the mature requests library
- **HttpHandler Interface** - `Callable[[Request], Response]` - same interface as servers
- **Session Management** - Efficient connection pooling and session handling
- **Full HTTP Support** - All HTTP methods, headers, and body types
- **Error Handling** - Converts requests exceptions to http4py responses

## Dependencies

- `http4py-core` - Core HTTP primitives
- `requests` - HTTP library for Python

## Usage

```python
from http4py.core import Request
from http4py.core.method import GET
from http4py.client_requests import RequestsClient

client = RequestsClient()
request = Request(GET, "https://api.example.com/users")
response = client(request)

print(f"Status: {response.status}")
print(f"Body: {response.body}")
```

## Testing

This package includes contract tests that ensure the client behaves consistently with the http4py specification:

```python
from http4py.client_requests import RequestsClient
from http4py.testing import HttpClientContract

class TestRequestsClient(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return RequestsClient()
```