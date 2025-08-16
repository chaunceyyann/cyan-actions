#!/bin/bash

# Script to create and push a new release
# Usage: ./scripts/create-release.sh <version>
# Example: ./scripts/create-release.sh v1.0.0

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 v1.0.0"
    exit 1
fi

VERSION=$1

# Validate version format
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format vX.Y.Z (e.g., v1.0.0)"
    exit 1
fi

echo "Creating release $VERSION..."

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Warning: You're not on the main branch. Current branch: $CURRENT_BRANCH"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "Error: Working directory is not clean. Please commit or stash your changes."
    exit 1
fi

# Check if tag already exists
if git tag -l | grep -q "^$VERSION$"; then
    echo "Error: Tag $VERSION already exists"
    exit 1
fi

# Update package.json version
echo "Updating package.json version..."
sed -i.bak "s/\"version\": \".*\"/\"version\": \"${VERSION#v}\"/" package.json
rm package.json.bak

# Commit version update
git add package.json
git commit -m "chore: bump version to $VERSION"

# Create and push tag
echo "Creating tag $VERSION..."
git tag $VERSION

echo "Pushing changes..."
git push origin main
git push origin $VERSION

echo "✅ Release $VERSION created and pushed!"
echo "The publish workflow will automatically create a GitHub release."
echo "Other repos can now use: uses: chaunceyyann/cyan-actions@$VERSION"
