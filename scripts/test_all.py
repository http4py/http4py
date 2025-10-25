#!/usr/bin/env python3

import subprocess
import sys
import tomllib


def main():
    # Read workspace configuration
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    members = config["tool"]["uv"]["workspace"]["members"]

    for member in members:
        print(f"Testing {member}...")
        result = subprocess.run(["python", "scripts/test_module.py", member], check=False)

        if result.returncode != 0:
            print(f"Tests failed for {member}!")
            sys.exit(result.returncode)

    print("All tests passed!")


if __name__ == "__main__":
    main()
