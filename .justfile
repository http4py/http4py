default:
    @just --list

check:
    uv run --package http4py-core python -m pytest core/tests/
    uv run --package http4py-core mypy core/src/
    uv run --package http4py-server-random python -m pytest server/random/tests/
    uv run --package http4py-server-random mypy server/random/src/
    uv run ruff check .
    uv run ruff format --check .
