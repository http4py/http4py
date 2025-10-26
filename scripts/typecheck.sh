#!/usr/bin/env bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <module_path>"
    exit 1
fi

module_path="$1"

pkg_name="${module_path//\//-}"
if [[ ! "$pkg_name" =~ ^http4py- ]]; then
    pkg_name="http4py-$pkg_name"
fi

echo "Type checking module: $pkg_name"
echo "Module path: $module_path"

echo "Running type check for $pkg_name..."
uv run --package "$pkg_name" mypy -p http4py

echo "Type check passed for $pkg_name"
