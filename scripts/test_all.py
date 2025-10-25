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
        # Convert directory path to package name
        pkg_name = member.replace("/", "-")
        if not pkg_name.startswith("http4py-"):
            pkg_name = f"http4py-{pkg_name}"

        test_path = f"{member}/tests/"

        # Check if tests directory exists
        if not Path(test_path).exists():
            print(f"Skipping {pkg_name} - no tests directory found at {test_path}")
            continue

        print(f"Testing {pkg_name}...")
        result = subprocess.run(
            ["uv", "run", "--package", pkg_name, "python", "-m", "pytest", test_path, "-v"], check=False
        )

        if result.returncode != 0:
            print(f"Tests failed for {pkg_name}!")
            sys.exit(result.returncode)

    print("All tests passed!")


if __name__ == "__main__":
    main()
