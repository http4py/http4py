#!/usr/bin/env python3

import subprocess
import sys
import tomllib
from pathlib import Path


def main():
    # Read workspace configuration
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    members = config["tool"]["uv"]["workspace"]["members"]

    for member in members:
        print(f"Type checking {member}...")
        result = subprocess.run(["python", "scripts/typecheck_module.py", member], check=False)

        if result.returncode != 0:
            print(f"Type check failed for {member}!")
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
