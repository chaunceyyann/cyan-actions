# GitHub Packages Setup Guide

This document explains how to use cyan-actions as a GitHub Package in other repositories.

## Overview

The cyan-actions repository is now set up to publish releases to GitHub Packages, allowing other repositories to use the actions and workflows without direct repository references.

## Files Added

- `action.yml` - Main action definition for the package
- `package.json` - Package metadata for GitHub Packages
- `.github/workflows/publish-release.yml` - Automated release publishing
- `scripts/create-release.sh` - Helper script for creating releases
- `examples/usage-example.yml` - Example usage in other repos

## How It Works

### 1. Publishing a Release

When you create and push a tag (e.g., `v1.0.0`), the `publish-release.yml` workflow automatically:

1. Creates a GitHub release
2. Publishes the package to GitHub Packages
3. Makes the version available to other repositories

### 2. Using in Other Repositories

Other repositories can now use your actions like this:

```yaml
# Using a workflow
jobs:
  python-tests:
    uses: chaunceyyann/cyan-actions@v1.0.0
    with:
      workflow: reusable-python-ci
      inputs: |
        {
          "python-version": "3.11",
          "run-integration-tests": true
        }

# Using an action
steps:
  - uses: chaunceyyann/cyan-actions@v1.0.0
    with:
      action: changed-files
      inputs: |
        {
          "pattern": "**/*.py"
        }
```

## Creating a Release

### Option 1: Using the Helper Script

```bash
./scripts/create-release.sh v1.0.0
```

### Option 2: Manual Process

```bash
# Update version in package.json
# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

## Benefits

1. **Private Repository Support**: Works even if cyan-actions is private
2. **Version Control**: Specific versions can be referenced
3. **Better Performance**: Cached by GitHub
4. **Professional**: Standard way to distribute GitHub Actions

## Migration from Direct References

### Before (Direct Repository Reference)
```yaml
uses: chaunceyyann/cyan-actions/.github/workflows/reusable-python-ci.yml@main
```

### After (GitHub Package Reference)
```yaml
uses: chaunceyyann/cyan-actions@v1.0.0
with:
  workflow: reusable-python-ci
  inputs: |
    {
      "python-version": "3.11"
    }
```

## Available Actions and Workflows

### Actions
- `changed-files`
- `account-mapping`
- `check-keywords`
- `check-codepipeline`
- `generate-report`
- `run-codepipeline`
- `test-actions`
- `test-workflows`
- `pr-status-commenter`

### Workflows
- `reusable-python-ci`
- `reusable-pre-commit`
- `reusable-terraform-lint`
- `reusable-pr-status-commenter`
- `reusable-plan-only-pipeline`

## Troubleshooting

### Common Issues

1. **Version not found**: Make sure the tag exists and the release was published
2. **Permission denied**: Ensure the repository has access to the package
3. **Invalid inputs**: Check the JSON format of the inputs parameter

### Debugging

- Check the GitHub release page for the specific version
- Verify the workflow ran successfully in the Actions tab
- Check the package manifest in the release assets
