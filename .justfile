default:
    @just --list

check:
    uv run python -m pytest
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy .
