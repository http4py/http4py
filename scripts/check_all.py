#!/usr/bin/env python3

import subprocess
import sys


def run_check(name, cmd):
    print(f"Running {name}...")
    result = subprocess.run(cmd, shell=True, check=False)
    if result.returncode != 0:
        print(f"{name} failed!")
        sys.exit(result.returncode)
    print(f"{name} passed!")


def main():
    run_check("tests", "python scripts/test_all.py")
    run_check("type checks", "python scripts/typecheck_all.py")
    run_check("linting", "uv run ruff check .")
    run_check("formatting", "uv run ruff format --check .")
    print("All checks passed!")


if __name__ == "__main__":
    main()
