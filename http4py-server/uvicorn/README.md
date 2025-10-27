# http4py-server-uvicorn

Uvicorn server implementation for http4py applications.

## Overview

This package provides a direct Uvicorn server integration for http4py applications, offering high-performance async HTTP serving with a simple, batteries-included approach.

### Components
- **UvicornServer** - Direct Uvicorn server implementation
- **Server Configuration** - Uvicorn-specific configuration options

## Features

- **High Performance** - Built on uvloop and httptools for maximum speed
- **Production Ready** - Battle-tested Uvicorn server under the hood
- **Simple Integration** - Direct http4py HttpHandler support
- **Flexible Configuration** - Full access to Uvicorn configuration options
- **Auto-reload** - Development mode with automatic reloading

## Dependencies

- `http4py-core` - Core HTTP primitives
- `http4py-server-asgi` - ASGI adapter
- `uvicorn` - Lightning-fast ASGI server

## Usage

### Basic Server

```python
from http4py.core import Request, Response
from http4py.core.status import OK
from http4py.server_uvicorn import UvicornServer

def hello_handler(request: Request) -> Response:
    return Response(OK).body_("Hello, Uvicorn!")

server = UvicornServer(port=8000, host="0.0.0.0")
server.serve(hello_handler).start().block()
```

### With Configuration

```python
from http4py.core import Response
from http4py.core.method import GET
from http4py.core.status import OK
from http4py.routing import route, routes
from http4py.server_uvicorn import UvicornServer

def api_handler(request):
    return Response(OK).body_('{"status": "ok"}').header_("Content-Type", "application/json")

app = routes(
    route("/api/health").bind(GET).to(api_handler)
)

# Production configuration
server = UvicornServer(
    port=8000,
    host="0.0.0.0",
    workers=4,
    access_log=True,
    log_level="info"
)

server.serve(app).start().block()
```

### Development Mode

```python
from http4py.server_uvicorn import UvicornServer

# Development with auto-reload
server = UvicornServer(
    port=8000,
    host="127.0.0.1",
    reload=True,
    log_level="debug"
)

server.serve(hello_handler).start().block()
```

## Configuration Options

The UvicornServer supports all standard Uvicorn configuration options:

- **host** - Bind socket to this host (default: "127.0.0.1")
- **port** - Bind socket to this port (default: 8000)
- **workers** - Number of worker processes (default: 1)
- **reload** - Enable auto-reload for development (default: False)
- **log_level** - Log level (default: "info")
- **access_log** - Enable access logging (default: False)

## Production Deployment

```python
# High-performance production setup
server = UvicornServer(
    port=8000,
    host="0.0.0.0",
    workers=4,  # Number of CPU cores
    access_log=True,
    log_level="warning"
)
```