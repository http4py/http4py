# http4py

A functional HTTP toolkit for Python, inspired by http4k. Provides immutable, composable HTTP primitives with a clean, functional API.

## Quick Start

### Installation
```bash
git clone <repository>
cd http4py
uv sync --dev
```

### Running Tests and Checks

#### Individual Module Testing
```bash
# Test a specific module
python scripts/test_module.py http4py-core
python scripts/test_module.py http4py-server/asgi
python scripts/test_module.py http4py-server/uvicorn

# Type check a specific module  
python scripts/typecheck_module.py http4py-core
python scripts/typecheck_module.py http4py-server/asgi
python scripts/typecheck_module.py http4py-server/uvicorn
```

#### Workspace-wide Testing
```bash
# Run all tests across all modules
python scripts/test_all.py

# Run all type checks across all modules
python scripts/typecheck_all.py

# Run everything (tests + type checks + linting + formatting)
python scripts/check_all.py
```

#### Using Just (Alternative)
```bash
# Complete workspace check
just check

# Individual module commands
just test-module http4py-core
just typecheck-module http4py-core

# Workspace-wide commands
just test-all
just typecheck-all
```

#### Direct uv Commands
```bash
# Individual package testing
uv run --package http4py-core python -m pytest http4py-core/tests/ -v
uv run --package http4py-server-asgi python -m pytest http4py-server/asgi/tests/ -v

# Type checking
uv run --package http4py-core mypy -p http4py

# Linting and formatting
uv run ruff check .
uv run ruff format .
```

## Architecture

This is a uv workspace with multiple packages:
- **`http4py-core`** - Core HTTP primitives (Request, Response, Uri, Status, etc.)
- **`http4py-server/asgi`** - ASGI server adapters  
- **`http4py-server/uvicorn`** - Uvicorn server implementation

## Development

### Adding New Modules
When you add a new package to the workspace:
1. Add it to `tool.uv.workspace.members` in `pyproject.toml`
2. The test scripts will automatically discover and include it

### Script Architecture
The testing system uses a composable approach:
- **Individual module scripts**: `test_module.py`, `typecheck_module.py`
- **Mega scripts**: `test_all.py`, `typecheck_all.py`, `check_all.py` compose the individual scripts
- **Templates**: All scripts read the workspace configuration dynamically

### CI/CD
GitHub Actions automatically:
- Tests each module individually using `test_module.py`
- Type checks each module using `typecheck_module.py`  
- Runs linting and formatting checks
- Builds packages on tagged releases