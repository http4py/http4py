#!/usr/bin/env python3

import os
import subprocess
import sys
import tomllib
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/typecheck_module.py <module_path>")
        print("Example: python scripts/typecheck_module.py http4py-core")
        sys.exit(1)
    
    module_path = sys.argv[1]
    
    # Read workspace configuration to build MYPYPATH
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    
    members = config["tool"]["uv"]["workspace"]["members"]
    
    # Build MYPYPATH from all src directories
    src_paths = []
    for member in members:
        src_path = f"{member}/src"
        if Path(src_path).exists():
            src_paths.append(src_path)
    
    mypy_path = ":".join(src_paths)
    
    # Convert directory path to package name
    pkg_name = module_path.replace("/", "-")
    if not pkg_name.startswith("http4py-"):
        pkg_name = f"http4py-{pkg_name}"
    
    print(f"Type checking module: {pkg_name}")
    print(f"Module path: {module_path}")
    
    # Run mypy type checking
    print(f"Running type check for {pkg_name}...")
    env = os.environ.copy()
    env["MYPYPATH"] = mypy_path
    
    result = subprocess.run([
        "uv", "run", "--package", pkg_name,
        "mypy", "-p", "http4py"
    ], env=env, check=False)
    
    if result.returncode != 0:
        print(f"Type check failed for {pkg_name}!")
        sys.exit(result.returncode)
    
    print(f"Type check passed for {pkg_name}")


if __name__ == "__main__":
    main()