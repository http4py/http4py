#!/usr/bin/env bash

set -e

show_help() {
    cat << EOF
http4py development script

Usage: $0 <command> [options]

Commands:
    test            Run tests for all packages
    test <module>   Run tests for specific module (e.g. http4py-core)
    typecheck       Run type checks for all packages
    typecheck <module>  Run type check for specific module
    lint            Run linting checks
    format          Auto-format code
    format-check    Check if code is formatted
    build           Build all packages
    check           Run all checks (test, typecheck, lint, format-check)
    release <type>  Release with version bump (patch|minor|major)
    clean           Clean build artifacts

Examples:
    $0 test                    # Test all packages
    $0 test http4py-core       # Test core package only
    $0 typecheck               # Type check all packages
    $0 build                   # Build all packages
    $0 release patch           # Release patch version
    $0 check                   # Run all quality checks

EOF
}

test() {
    local module="$1"
    ./scripts/test.sh "$module"
}

typecheck() {
    local module="$1"
    ./scripts/typecheck.sh "$module"
}

lint() {
    echo "Running linting..."
    uv run ruff check .
    echo "Linting passed!"
}

format() {
    echo "Auto-formatting code..."
    uv run ruff format .
}

format-check() {
    echo "Checking formatting..."
    uv run ruff format --check .
    echo "Formatting passed!"
}

build() {
    local module="$1"
    ./scripts/build.sh "$module"
}

clean() {
    echo "Cleaning build artifacts..."
    rm -rf dist/ .pytest_cache/ **/.pytest_cache/ **/__pycache__/
    echo "Clean completed!"
}

release() {
    local bump_type="$1"
    ./scripts/release.sh "$bump_type"
}

main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi

    case "$1" in
        check)
            "$0" test
            "$0" typecheck
            lint
            format
            format-check
            ;;
        test|typecheck|build)
            if [ $# -eq 1 ]; then
                command="$1"
                for member in $(yq eval '.tool.uv.workspace.members[]' pyproject.toml); do
                    echo "Running $command for $member..."
                    if ! "$command" "$member"; then
                        echo "$command failed for $member!"
                        exit 1
                    fi
                done

                if [ "$command" = "typecheck" ] && [ -d "examples/" ]; then
                    echo "Type checking examples..."
                    uv run mypy examples/
                fi

                echo "All $command operations passed!"
            else
                # Run command for specific module
                "$1" "$2"
            fi
            ;;
        lint)
            lint
            ;;
        format)
            format
            ;;
        format-check)
            format-check
            ;;
        clean)
            clean
            ;;
        release)
            release "$2"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "Unknown command: $1"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"
