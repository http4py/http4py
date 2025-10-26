#!/usr/bin/env bash

set -e

run_command() {
    local description="$1"
    shift
    
    echo "Running $description..."
    if "$@"; then
        echo "$description completed!"
    else
        echo "$description failed!"
        exit 1
    fi
}

get_current_version() {
    yq eval '.project.version' pyproject.toml
}

bump_version() {
    local current_version="$1"
    local bump_type="$2"
    
    IFS='.' read -r major minor patch <<< "$current_version"
    
    case "$bump_type" in
        major)
            echo "$((major + 1)).0.0"
            ;;
        minor)
            echo "$major.$((minor + 1)).0"
            ;;
        patch)
            echo "$major.$minor.$((patch + 1))"
            ;;
        *)
            echo "Invalid bump type: $bump_type" >&2
            exit 1
            ;;
    esac
}

update_version() {
    local new_version="$1"
    
    echo "Updating version to $new_version in all packages..."
    
    # Update tool.http4py.common version in root
    sed -i '' "/\[tool\.http4py\.common\]/,/^\[/ s/version = \"[^\"]*\"/version = \"$new_version\"/" pyproject.toml
    
    # Update version in each workspace member
    for member in $(yq eval '.tool.uv.workspace.members[]' pyproject.toml); do
        echo "Updating version in $member..."
        sed -i '' "s/version = \"[^\"]*\"/version = \"$new_version\"/" "$member/pyproject.toml"
    done
}

run_checks() {
    echo "Running all checks before release..."
    ./scripts/http4py.sh check
}

build_packages() {
    echo "Building all packages..."
    ./scripts/http4py.sh build
}

create_git_tag() {
    local version="$1"
    
    echo "Creating git tag v$version..."
    git add .
    git commit -m "Release v$version"
    git tag "v$version"
}

publish_packages() {
    echo "Publishing packages to PyPI..."
    uv publish
}

main() {
    if [ $# -ne 1 ]; then
        echo "Usage: $0 <bump_type>"
        echo "bump_type: major, minor, or patch"
        echo "Example: $0 patch"
        exit 1
    fi
    
    local bump_type="$1"
    if [[ ! "$bump_type" =~ ^(major|minor|patch)$ ]]; then
        echo "bump_type must be one of: major, minor, patch"
        exit 1
    fi
    
    # Get current version and calculate new version
    local current_version
    current_version=$(get_current_version)
    local new_version
    new_version=$(bump_version "$current_version" "$bump_type")
    
    echo "Current version: $current_version"
    echo "New version: $new_version"
    
    # Confirm with user
    read -p "Release version $new_version? (y/N): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Release cancelled."
        exit 0
    fi
    
    # Check git status
    if [ -n "$(git status --porcelain)" ]; then
        echo "Warning: Working directory has uncommitted changes!"
        read -p "Continue anyway? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Release cancelled."
            exit 0
        fi
    fi
    
    # Run pre-release checks
    run_checks
    
    # Update version
    update_version "$new_version"
    
    # Build packages
    build_packages
    
    # Create git tag
    create_git_tag "$new_version"
    
    # Ask about publishing
    read -p "Publish to PyPI? (y/N): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        publish_packages
        echo "Successfully released version $new_version!"
        echo "Don't forget to push: git push origin v$new_version"
    else
        echo "Version $new_version prepared but not published."
        echo "To publish later, run: uv publish"
        echo "To push tags, run: git push origin v$new_version"
    fi
}

main "$@"