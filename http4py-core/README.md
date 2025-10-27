# http4py-core

The core HTTP toolkit providing immutable, composable HTTP primitives.

## Overview

This package contains the fundamental building blocks of http4py:

### HTTP Messages
- **Request** - Immutable HTTP request with method, URI, headers, and body
- **Response** - Immutable HTTP response with status, headers, and body
- **Body** - Abstract body handling for memory and streaming content

### HTTP Primitives
- **Method** - HTTP methods enum (GET, POST, PUT, DELETE, etc.)
- **Status** - HTTP status codes enum (OK, NOT_FOUND, INTERNAL_SERVER_ERROR, etc.)
- **Uri** - Immutable URI with parsing and builder methods
- **HttpVersion** - HTTP version enumeration

### Core Interfaces
- **HttpHandler** - `Callable[[Request], Response]` - unified interface for servers and clients

### Server Components
- **Http4pyServer** - Abstract server interface
- **ServerConfig** - Abstract server configuration
- **StdLibServer** - Standard library HTTP server implementation

### Client Components
- **python_client** - HTTP client using urllib

### Routing
- **Route** - Path-based routing with fluent API
- **RoutingHttpHandler** - Handler that dispatches based on routes

### Filters
- **debug** - Request/response debugging filter

## Key Features

- **Immutable** - All HTTP objects are frozen dataclasses
- **Functional** - Builder pattern with fluent API (`method_()` returns new instance)
- **Type Safe** - Full type annotations with mypy strict mode
- **Composable** - Mix and match components as needed

## Usage

```python
from http4py.core import Request, Response
from http4py.core.method import GET
from http4py.core.status import OK

# Create immutable request
request = Request(GET, "/api/users").header_("Authorization", "Bearer token")

# Create immutable response
response = Response(OK).body_("Hello World").header_("Content-Type", "text/plain")
```