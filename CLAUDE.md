# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# http4py - Python HTTP Toolkit

## Project Overview

http4py is a functional HTTP toolkit for Python, inspired by the http4k library. It provides immutable, composable HTTP primitives with a clean, functional API.

## Architecture

### Package Structure
This is a uv workspace with multiple packages that follow a modular monorepo structure:

- **`http4py-core`** - Core HTTP primitives (Request, Response, Uri, Status, Method, etc.)
- **`http4py-testing/support`** - Shared testing utilities and contracts for cross-package testing
- **`http4py-client/requests`** - HTTP client using requests library
- **`http4py-server/asgi`** - ASGI server adapters
- **`http4py-server/uvicorn`** - Uvicorn server implementation

### Key Design Principles
- **Immutability** - All HTTP objects are immutable using frozen dataclasses
- **Functional composition** - Builder pattern with fluent API
- **Server as a Function** - HttpHandler = Callable[[Request], Response] - same interface for servers and clients
- **Type safety** - Full type annotations with mypy strict mode
- **Separation of concerns** - Core HTTP vs routing vs server vs client concerns are separate
- **Enum-based constants** - Use enums with convenience constants for HTTP methods and status codes
- **Test contracts** - Use abstract base classes to ensure consistent behavior across implementations

## Development Commands

### Main Development Script
Use `./scripts/http4py.sh` for all development tasks. This script handles workspace operations across all packages:

#### Testing
```bash
./scripts/http4py.sh test                    # Test all packages
./scripts/http4py.sh test http4py-core       # Test specific package
./scripts/http4py.sh test core               # Also works (auto-prefixes http4py-)
```

#### Type Checking
```bash
./scripts/http4py.sh typecheck               # Type check all packages + examples
./scripts/http4py.sh typecheck http4py-core  # Type check specific package
```

#### Code Quality
```bash
./scripts/http4py.sh lint                    # Run ruff linting
./scripts/http4py.sh format                  # Auto-format with ruff
./scripts/http4py.sh format-check            # Check formatting
./scripts/http4py.sh check                   # Run ALL checks (test + typecheck + lint + format)
```

#### Build and Release
```bash
./scripts/http4py.sh build                   # Build all packages
./scripts/http4py.sh build http4py-core      # Build specific package
./scripts/http4py.sh clean                   # Clean build artifacts
./scripts/http4py.sh release patch           # Release with version bump
```

### Direct UV Commands (Alternative)
```bash
uv run pytest                               # Run all tests
uv run --package http4py-core pytest        # Test specific package
uv run --package http4py-core mypy -p http4py  # Type check specific package
uv run ruff check .                         # Lint
uv run ruff format .                        # Format
uv build --package http4py-core             # Build package
```

## Code Style Guidelines

### Code Style Requirements
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

### Example Code Pattern
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

### Test Contracts Architecture
- **Testing support package** - Use `http4py-testing-support` package for shared testing utilities and contracts
- **Contract naming** - Use `contract_*` prefix for test contract files (e.g., `contract_http_client.py`)
- **Abstract base classes** - Use ABC to define behavioral contracts that implementations must satisfy
- **Import pattern** - Import shared contracts: `from http4py.testing import HttpClientContract`
- **Implementation testing** - Each implementation extends the contract to ensure consistent behavior
- **Integration testing** - Use real servers/clients instead of mocks for contract tests when possible
- **Dev dependencies** - Packages add `http4py-testing-support` as dev dependency for testing

### Contract Example
```python
from __future__ import annotations

from http4py.client import StdLibClient
from http4py.core import HttpHandler
from http4py.testing import HttpClientContract

class TestPythonClient(HttpClientContract):
    def create_client(self) -> HttpHandler:
        return StdLibClient()
```

## Core Components Architecture

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

### Workspace Package Organization
- **Core Package** (`http4py-core`) - Contains fundamental HTTP primitives and base abstractions
- **Client Packages** (`http4py-client/*`) - HTTP client implementations (requests, etc.)
- **Server Packages** (`http4py-server/*`) - Server implementations (ASGI, uvicorn, etc.)
- **Testing Package** (`http4py-testing/support`) - Shared test contracts and utilities

## Important Implementation Reminders

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

## Workspace Development Patterns

### Cross-Package Development
- Use the main development script `./scripts/http4py.sh` for operations across packages
- The script automatically handles package name normalization (e.g., "core" becomes "http4py-core")
- Dependencies between packages are managed via `[tool.uv.sources]` workspace references
- Testing support package provides shared contracts for consistent behavior across implementations

### Package-Specific Operations
- Use `uv run --package <package-name>` for package-specific operations
- Each package has its own `pyproject.toml` with build configuration
- Testing contracts ensure implementations behave consistently across different packages
- Type checking runs per-package plus examples directory

### Tool Configuration
- **Python 3.13+** minimum version across all packages
- **uv** for package management and virtual environments
- **pytest** for testing with shared configuration in root pyproject.toml
- **mypy** in strict mode with workspace-wide configuration
- **ruff** for linting and formatting with consistent rules
- **hatchling** for building packages