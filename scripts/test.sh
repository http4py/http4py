#!/usr/bin/env bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <module_path>"
    echo "Example: $0 http4py-core"
    exit 1
fi

module_path="$1"

pkg_name="${module_path//\//-}"
if [[ ! "$pkg_name" =~ ^http4py- ]]; then
    pkg_name="http4py-$pkg_name"
fi

test_path="$module_path/tests/"

echo "Testing module: $pkg_name"
echo "Module path: $module_path"

if [ ! -d "$test_path" ]; then
    echo "No tests directory found at $test_path, skipping tests"
    exit 0
fi

echo "Running tests for $pkg_name..."
uv run --package "$pkg_name" python -m pytest "$test_path" -v

echo "Tests passed for $pkg_name"
