#!/usr/bin/env python3

import os
import subprocess
import sys
import tomllib
from pathlib import Path


def main():
    # Read workspace configuration
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

    for member in members:
        # Convert directory path to package name
        pkg_name = member.replace("/", "-")
        if not pkg_name.startswith("http4py-"):
            pkg_name = f"http4py-{pkg_name}"

        print(f"Type checking {pkg_name}...")

        # Set environment with MYPYPATH
        env = os.environ.copy()
        env["MYPYPATH"] = mypy_path

        result = subprocess.run(["uv", "run", "--package", pkg_name, "mypy", "-p", "http4py"], env=env, check=False)

        if result.returncode != 0:
            print(f"Type check failed for {pkg_name}!")
            sys.exit(result.returncode)

    # Type check examples if directory exists
    if Path("examples/").exists():
        print("Type checking examples...")
        result = subprocess.run(["uv", "run", "mypy", "examples/"], check=False)
        if result.returncode != 0:
            print("Type check failed for examples!")
            sys.exit(result.returncode)

    print("All type checks passed!")


if __name__ == "__main__":
    main()
