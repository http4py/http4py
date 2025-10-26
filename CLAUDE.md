# http4py - Python HTTP Toolkit

## Project Overview

http4py is a functional HTTP toolkit for Python, inspired by the http4k library. It provides immutable, composable HTTP primitives with a clean, functional API.

## Architecture

### Package Structure
- **`http4py.core`** - Core HTTP primitives (Request, Response, Uri, Status, Method, etc.)
- **`http4py.routing`** - Routing functionality (Route, route, RoutingHttpHandler, routes)
- **`http4py.server`** - Server abstractions and implementations (Http4pyServer, StdLib)
- **`http4py.client`** - HTTP client implementations (stdlib_client)

### Key Design Principles
- **Immutability** - All HTTP objects are immutable using frozen dataclasses
- **Functional composition** - Builder pattern with fluent API
- **Server as a Function** - HttpHandler = Callable[[Request], Response] - same interface for servers and clients
- **Type safety** - Full type annotations with mypy strict mode
- **Separation of concerns** - Core HTTP vs routing vs server vs client concerns are separate
- **Enum-based constants** - Use enums with convenience constants for HTTP methods and status codes
- **Test contracts** - Use abstract base classes to ensure consistent behavior across implementations

## Style Guide

### Code Style
- **NO COMMENTS** - Code should be self-documenting
- **Future annotations MANDATORY** - Always use `from __future__ import annotations` as first import
- **NO QUOTED TYPE NAMES** - Never use quotes around type names (e.g., `-> Request` not `-> "Request"`)
- **Frozen dataclasses** - Use `@dataclass(frozen=True)` for immutability
- **Builder pattern** - Methods ending with `_` return new instances
- **120 character line length**
- **Double quotes** for strings
- **Space indentation**

### Type Annotations
- **Complete typing** - All functions must have full type annotations
- **Strict mypy** - Code must pass mypy in strict mode
- **Return types** - All methods must specify return types
- **Object parameter** - Use `other: object` for `__eq__` methods
- **Explicit re-exports** - Use `import Name as Name` syntax for mypy strict mode compatibility

### Import Style
```python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Union
```

### Example Code Style
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, init=False)
class Example:
    value: str

    def __init__(self, value: str):
        object.__setattr__(self, "value", value)

    def _copy(self, **overrides: Any) -> Example:
        return Example(overrides.get("value", self.value))

    def value_(self, new_value: str) -> Example:
        return self._copy(value=new_value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Example):
            return False
        return self.value == other.value
```

## Testing Guidelines

### Test Contracts
- **Contract naming** - Use `contract_*` prefix for test contract files (e.g., `contract_http_client.py`)
- **Shared contracts** - Place shared test contracts in the core package tests for cross-package access
- **Abstract base classes** - Use ABC to define behavioral contracts that implementations must satisfy
- **Import pattern** - Import shared contracts: `from http4py.client.contract_http_client import ContractName`
- **Implementation testing** - Each implementation extends the contract to ensure consistent behavior
- **Integration testing** - Use real servers/clients instead of mocks for contract tests when possible

### Contract Example
```python
from __future__ import annotations

from abc import ABC, abstractmethod
from http4py.core import HttpHandler, Request, Response

class HttpClientContract(ABC):
    @abstractmethod
    def create_client(self) -> HttpHandler:
        pass

    def test_simple_get_request(self) -> None:
        client = self.create_client()
        # Test implementation...

class TestPythonClient(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return PythonClient()
```

## Development Setup

### Tools Configuration
- **uv** - Package management and virtual environments
- **pytest** - Testing framework
- **mypy** - Type checking (strict mode)
- **ruff** - Linting and formatting
- **Python 3.13+** - Minimum version

### Running Tests
```bash
uv run python -m pytest -v --tb=short
```

### Type Checking
```bash
uv run mypy core/src/http4py
```

### Linting and Formatting
```bash
uv run ruff check .
uv run ruff format .
```

## Core Components

### HTTP Messages
- **Request** - HTTP request with method, uri, headers, body
- **Response** - HTTP response with status, headers, body
- **Body** - Abstract body handling (memory/stream)

### HTTP Primitives
- **Method** - HTTP methods enum with constants (Method.GET, GET, etc.)
- **Status** - HTTP status codes enum with constants (Status.OK, OK, etc.)
- **HttpVersion** - HTTP version enumeration
- **HttpHandler** - Core functional interface: Callable[[Request], Response]
- **Uri** - Immutable URI with `Uri.of()` parsing and builder methods

### Server Components
- **Http4pyServer** - Abstract server interface with start/stop/block methods
- **ServerConfig** - Abstract configuration interface
- **StdLib** - Standard library HTTP server implementation

### Client Components
- **stdlib_client** - HTTP client as HttpHandler using urllib.request

### Routing
- **Route** - Path-based routing with fluent API
- **RoutingHttpHandler** - Handler that dispatches based on routes

## Usage Examples

### Basic Request/Response
```python
from http4py.core import Request, Response
from http4py.core.method import GET
from http4py.core.status import OK

request = Request(GET, "/api/users").header_("Authorization", "Bearer token")
response = Response(OK).body_("Hello World").header_("Content-Type", "text/plain")
```

### Server
```python
from http4py.core import Response
from http4py.core.status import OK
from http4py.server import StdLib

def hello_handler(request):
    return Response(OK).body_("Hello, http4py!")

StdLib(8080).serve(hello_handler).start().block()
```

### Client
```python
from http4py.core import Request
from http4py.core.method import GET
from http4py.client import stdlib_client

request = Request(GET, "https://api.example.com/users")
response = stdlib_client(request)
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

### URI Building
```python
from http4py.core import Uri

# Simple string URIs (preferred for most cases)
request = Request(GET, "https://api.example.com/users?active=true&limit=10")

# Builder pattern for dynamic construction
uri = (Uri.of("https://api.example.com")
    .path_("/users")
    .query_("active", "true")
    .query_("limit", "10"))

print(str(uri))  # https://api.example.com/users?active=true&limit=10
```

## CI/CD

GitHub Actions workflow automatically:
- Runs tests on Python 3.13
- Performs type checking with mypy
- Runs linting with ruff
- Builds packages
- Uploads build artifacts

## Commands Reference

### Package Management
```bash
uv sync --dev              # Install dependencies
uv add <package>           # Add dependency
uv build                   # Build package
```

### Testing
```bash
uv run pytest             # Run all tests
uv run pytest -v          # Verbose output
uv run pytest path/       # Run specific tests
```

### Quality Checks
```bash
uv run mypy core/src/      # Type checking
uv run ruff check .        # Linting
uv run ruff format .       # Auto-formatting
```

## Important Reminders

1. **Always use `from __future__ import annotations`**
2. **Never add comments to code**
3. **All dataclasses must be frozen**
4. **All methods must have complete type annotations**
5. **Use builder pattern with trailing `_` for mutator methods**
6. **Separate core HTTP concerns from routing/server/client concerns**
7. **Code must pass mypy strict mode**
8. **Use double quotes for strings**
9. **120 character line limit**
10. **Use explicit re-exports (`import Name as Name`) for mypy strict compatibility**
11. **Constants co-located with enums** - HTTP status/method constants live in their respective enum modules
12. **Server as a Function design** - HttpHandler interface unifies servers and clients
13. **Import from specific modules** - Use `from http4py.core.status import OK` not convenience wrappers
14. **Enum-based lookups** - Use `Status.from_code()` for dynamic status creation
15. **Prefer string URIs** - Use `Request(GET, "https://example.com")` over builder pattern for simple cases
16. **Uri.of() for parsing** - Use `Uri.of()` method instead of deprecated `Uri.parse()`
17. **Do not explicitly reference modules in root pyproject.toml except in workspace member list**
