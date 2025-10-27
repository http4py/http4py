# http4py-server-asgi

ASGI server adapters for http4py applications.

## Overview

This package provides ASGI (Asynchronous Server Gateway Interface) adapters that allow http4py applications to run on ASGI-compliant servers like Uvicorn, Hypercorn, and Daphne.

### Components
- **AsgiAdapter** - Converts http4py HttpHandler to ASGI application
- **StandardAsgiAdapter** - Standard implementation of ASGI adapter

## Features

- **ASGI Compliance** - Full ASGI 3.0 specification support
- **HttpHandler Bridge** - Seamless integration with http4py applications
- **Async Support** - Handles asynchronous request/response processing
- **Server Agnostic** - Works with any ASGI-compliant server

## Dependencies

- `http4py-core` - Core HTTP primitives
- `asgiref` - ASGI reference implementation

## Usage

### Basic ASGI Application

```python
from http4py.core import Request, Response
from http4py.core.status import OK
from http4py.server_asgi import AsgiAdapter

def hello_handler(request: Request) -> Response:
    return Response(OK).body_("Hello, ASGI!")

# Create ASGI application
asgi_app = AsgiAdapter(hello_handler)

# Run with uvicorn
# uvicorn main:asgi_app --host 0.0.0.0 --port 8000
```

### With Routing

```python
from http4py.core import Response
from http4py.core.method import GET
from http4py.core.status import OK
from http4py.routing import route, routes
from http4py.server_asgi import AsgiAdapter

def hello_handler(request):
    return Response(OK).body_("Hello!").header_("Content-Type", "text/plain")

def api_handler(request):
    return Response(OK).body_('{"message": "API"}').header_("Content-Type", "application/json")

app = routes(
    route("/hello").bind(GET).to(hello_handler),
    route("/api").bind(GET).to(api_handler)
)

asgi_app = AsgiAdapter(app)
```

## Deployment

### Uvicorn
```bash
uvicorn main:asgi_app --host 0.0.0.0 --port 8000
```

### Hypercorn
```bash
hypercorn main:asgi_app --bind 0.0.0.0:8000
```

### Daphne
```bash
daphne -b 0.0.0.0 -p 8000 main:asgi_app
```