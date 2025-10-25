#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/test_module.py <module_path>")
        print("Example: python scripts/test_module.py http4py-core")
        sys.exit(1)
    
    module_path = sys.argv[1]
    
    # Convert directory path to package name
    pkg_name = module_path.replace("/", "-")
    if not pkg_name.startswith("http4py-"):
        pkg_name = f"http4py-{pkg_name}"
    
    test_path = f"{module_path}/tests/"
    
    print(f"Testing module: {pkg_name}")
    print(f"Module path: {module_path}")
    
    # Check if tests directory exists
    if not Path(test_path).exists():
        print(f"No tests directory found at {test_path}, skipping tests")
        return
    
    print(f"Running tests for {pkg_name}...")
    result = subprocess.run([
        "uv", "run", "--package", pkg_name,
        "python", "-m", "pytest", test_path, "-v"
    ], check=False)
    
    if result.returncode != 0:
        print(f"Tests failed for {pkg_name}!")
        sys.exit(result.returncode)
    
    print(f"Tests passed for {pkg_name}")


if __name__ == "__main__":
    main()