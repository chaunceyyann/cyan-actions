#!/bin/bash

# Setup script for pre-commit hooks and JIRA integration

set -e  # Exit on any error

echo "🚀 Setting up pre-commit hooks and JIRA integration..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit is not installed."
    echo "Attempting to install with pip..."

    # Try to install with pip
    if command -v pip &> /dev/null; then
        pip install pre-commit
        echo "✅ pre-commit installed with pip"
    elif command -v pip3 &> /dev/null; then
        pip3 install pre-commit
        echo "✅ pre-commit installed with pip3"
    else
        echo "❌ pip not found. Please install pre-commit manually:"
        echo "  pip install pre-commit"
        echo "  or"
        echo "  brew install pre-commit"
        exit 1
    fi
else
    echo "✅ pre-commit is already installed"
fi

# Make the hook script executable
chmod +x hooks/commit-msg.sh
echo "✅ Made commit-msg.sh hook executable"

# Install pre-commit hooks
echo "📦 Installing pre-commit hooks..."
pre-commit install

echo "✅ Pre-commit hooks installed"

# Run pre-commit checks
if [ -n "$1" ]; then
    echo "🔍 Running pre-commit checks on changed files: $1"
    pre-commit run --files $1
else
    echo "🔍 Running pre-commit checks on all files..."
    pre-commit run --all-files
fi

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
