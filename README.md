# http4py

A functional HTTP toolkit for Python, inspired by http4k. Provides immutable, composable HTTP primitives with a clean, functional API.

## Installation

```bash
git clone <repository>
cd http4py
uv sync --dev
```

## Architecture

This is a uv workspace with multiple packages:

### Core Packages
- **`http4py-core`** - Core HTTP primitives (Request, Response, Uri, Status, Method, etc.)
- **`http4py-testing/support`** - Shared testing utilities and contracts

### Client Packages
- **`http4py-client/requests`** - HTTP client using requests library

### Server Packages
- **`http4py-server/asgi`** - ASGI server adapters
- **`http4py-server/uvicorn`** - Uvicorn server implementation

## Development Script

Use the `./scripts/http4py.sh` script for all development tasks:

### Basic Commands
```bash
./scripts/http4py.sh test                    # Test all packages
./scripts/http4py.sh test http4py-core       # Test specific package
./scripts/http4py.sh typecheck               # Type check all packages
./scripts/http4py.sh typecheck http4py-core  # Type check specific package
./scripts/http4py.sh check                   # Run all checks (test + typecheck + lint + format)
```

### Code Quality
```bash
./scripts/http4py.sh lint                    # Run linting checks
./scripts/http4py.sh format                  # Auto-format code
./scripts/http4py.sh format-check            # Check if code is formatted
```

### Build and Release
```bash
./scripts/http4py.sh build                   # Build all packages
./scripts/http4py.sh build http4py-core      # Build specific package
./scripts/http4py.sh release patch           # Release with patch version bump
./scripts/http4py.sh clean                   # Clean build artifacts
```

### Help
```bash
./scripts/http4py.sh help                    # Show all available commands
```

## Example Usage

### Simple Server
```python
from http4py.core import Request, Response
from http4py.core.status import OK
from http4py.server import StdLibServer

def hello_handler(request: Request) -> Response:
    return Response(OK).body_("Hello, http4py!")

StdLibServer(8080).serve(hello_handler).start().block()
```

### HTTP Client
```python
from http4py.core import Request
from http4py.core.method import GET
from http4py.client import python_client

request = Request(GET, "https://api.example.com/users")
response = python_client(request)
print(f"Status: {response.status}")
```

### Routing
```python
from http4py.core import Response
from http4py.core.method import GET
from http4py.core.status import OK
from http4py.routing import route, routes

def hello_handler(request):
    return Response(OK).body_("Hello!").header_("Content-Type", "text/plain")

app = routes(
    route("/hello").bind(GET).to(hello_handler)
)
```