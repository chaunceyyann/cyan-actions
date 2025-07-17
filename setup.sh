#!/bin/bash

# Setup script for pre-commit hooks and JIRA integration

set -e  # Exit on any error

echo "🚀 Setting up pre-commit hooks and JIRA integration..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit is not installed."
    echo "Please install it first:"
    echo "  pip install pre-commit"
    echo "  or"
    echo "  brew install pre-commit"
    exit 1
fi

echo "✅ pre-commit is installed"

# Make the hook script executable
chmod +x hooks/prepare-commit-msg
echo "✅ Made prepare-commit-msg hook executable"

# Install pre-commit hooks
echo "📦 Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type prepare-commit-msg

echo "✅ Pre-commit hooks installed"

# Run pre-commit on all files to ensure everything is set up
echo "🔍 Running pre-commit checks on all files..."
pre-commit run --all-files

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Your JIRA commit hook is now active. When you commit:"
echo "  - Branch: feature/ABC-123-description"
echo "  - Commit: git commit -m 'add login feature'"
echo "  - Result: [ABC-123] add login feature"
echo ""
echo "To test the hook:"
echo "  git checkout -b feature/ABC-123-test"
echo "  git commit --allow-empty -m 'test commit'"
echo ""
echo "For more information, see README.md"
