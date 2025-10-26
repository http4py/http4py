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

echo "Building package: $pkg_name"
echo "Module path: $module_path"

uv build --package "$pkg_name"

echo "Build completed for $pkg_name"
