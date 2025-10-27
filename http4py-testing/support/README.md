# http4py-testing-support

Shared testing utilities and contracts for http4py implementations.

## Overview

This package provides reusable testing utilities and behavioral contracts that ensure consistent behavior across all http4py implementations. It contains abstract base classes that define expected behavior for HTTP clients, servers, and other components.

### Components
- **HttpClientContract** - Abstract test contract for HTTP clients
- **HttpServerContract** - Abstract test contract for HTTP servers  
- **Testing Utilities** - Common testing helpers and fixtures

## Features

- **Behavioral Contracts** - Abstract base classes defining expected behavior
- **Cross-Package Testing** - Shared contracts ensure consistency across implementations
- **Test Utilities** - Common helpers for HTTP testing scenarios
- **Implementation Agnostic** - Works with any http4py implementation

## Dependencies

- `http4py-core` - Core HTTP primitives
- `pytest` - Testing framework

## Usage

### HTTP Client Contract

```python
from http4py.core import HttpHandler
from http4py.testing import HttpClientContract
from http4py.client_requests import RequestsClient

class TestRequestsClient(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return RequestsClient()
```

### HTTP Server Contract

```python
from http4py.core import HttpHandler
from http4py.testing import HttpServerContract
from http4py.server_uvicorn import UvicornServer

class TestUvicornServer(HttpServerContract):
    def create_server(self, handler: HttpHandler) -> Http4pyServer:
        return UvicornServer(port=0).serve(handler)
```

### Custom Testing

```python
from http4py.testing import create_test_request, create_test_response

def test_my_handler():
    request = create_test_request(GET, "/test")
    response = my_handler(request)
    assert response.status == OK
```

## Contract Testing

The contracts define standard test scenarios that all implementations must pass:

### Client Contract Tests
- Basic GET requests
- POST requests with body
- Header handling
- Error scenarios
- Timeout handling

### Server Contract Tests
- Request routing
- Response handling
- Error responses
- Concurrent requests
- Graceful shutdown

## Implementation Guide

When creating new http4py implementations:

1. **Extend the Contract** - Inherit from the appropriate contract class
2. **Implement Factory Method** - Provide a method to create your implementation
3. **Run Contract Tests** - All contract tests must pass
4. **Add Custom Tests** - Add implementation-specific tests as needed

## Benefits

- **Consistency** - Ensures all implementations behave the same way
- **Quality Assurance** - Comprehensive test coverage for core functionality
- **Integration Testing** - Real servers and clients, not mocks
- **Regression Prevention** - Catches breaking changes across the ecosystem