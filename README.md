# Shared GitHub Actions Workflows & Custom Actions

This repository serves as a central hub for all my shared [GitHub Actions](https://github.com/features/actions) workflows and custom actions. The goal is to provide reusable, well-documented automation building blocks for use across multiple projects.

## Purpose

- **Centralize**: Host all shared workflows and custom actions in one place.
- **Reuse**: Make it easy to include and update workflows across repositories.
- **Customize**: Provide tailored automation solutions for common CI/CD needs.

## Usage

You can reference workflows or actions from this repository in your own projects. For example:

### Reusing a Workflow

To reuse a workflow from this repository, use the `uses` keyword in your workflow YAML:

```yaml
# .github/workflows/your-workflow.yml
name: Use Shared Workflow
on:
  push:
    branches: [ main ]
jobs:
  call-shared-workflow:
    uses: chaunceyyann/cyan-actions/.github/workflows/shared-workflow.yml@master
    with:
      example-input: "Hello, World!"        # replace with real inputs
    secrets:
      example-secret: ${{ secrets.MY_SECRET }}  # replace with real secrets
```

### Using a Custom Action

To use a custom action from this repository, reference its path and version in your workflow steps:

```yaml
# .github/workflows/your-workflow.yml
name: Use Custom Action
on:
  push:
    branches: [ main ]
jobs:
  use-custom-action:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: chaunceyyann/cyan-actions/path/to/custom-action@master
        with:
          action-input: "Some value"          # replace with real inputs
```

> **Note**: Update `shared-workflow.yml` and `path/to/custom-action` to the actual file/action paths, and adjust inputs/secrets as needed.

## Status

[![Build Status](https://github.com/chaunceyyann/cyan-actions/actions/workflows/ci.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions)


---

Feel free to contribute or suggest improvements!

# GitHub Actions Repository

This repository contains shared GitHub Actions workflows and custom actions for CI/CD automation.

## Features

- **Custom Actions**: Reusable composite actions for common tasks
- **Shared Workflows**: Standardized CI/CD workflows
- **Account Mapping**: Environment-aware AWS account routing
- **Git Hooks**: Automated commit message formatting with JIRA integration

## Quick Start

### 1. Install pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Or with Homebrew (macOS)
brew install pre-commit
```

### 2. Install Git hooks

```bash
# Install the pre-commit hooks
pre-commit install

# Install the prepare-commit-msg hook specifically
pre-commit install --hook-type prepare-commit-msg
```

### 3. Verify installation

```bash
# Check installed hooks
pre-commit run --all-files

# Test the prepare-commit-msg hook
git commit --allow-empty -m "test commit"
```

## Using the JIRA Commit Hook

The `prepare-commit-msg` hook automatically adds JIRA ticket numbers to commit messages based on your branch name.

### Branch Naming Examples

| Branch Name | JIRA Ticket | Commit Message Result |
|-------------|-------------|----------------------|
| `feature/ABC-123-add-login` | ABC-123 | `[ABC-123] your message` |
| `bugfix/PROJECT-456-fix-bug` | PROJECT-456 | `[PROJECT-456] your message` |
| `hotfix/ABC789-critical-fix` | ABC-789 | `[ABC-789] your message` |
| `feature/ABC123-description` | ABC-123 | `[ABC-123] your message` |

### Supported Patterns

- **Standard**: `JIRA-123`, `ABC-456`
- **No dash**: `ABC123`, `PROJECT456` (auto-converts to `ABC-123`)
- **Custom**: `AB-123` (at least 2 letters)

### Skipped Commits

The hook automatically skips:
- Merge commits
- Revert commits
- Commits starting with: `Merge`, `Revert`, `WIP`, `Draft`

### Manual Testing

```bash
# Create a test branch with JIRA ticket
git checkout -b feature/ABC-123-test-hook

# Make a commit
git commit --allow-empty -m "test commit message"

# Should see: ✅ Added JIRA ticket [ABC-123] to commit message from branch: feature/ABC-123-test-hook
```

## Custom Actions

### Account Mapping Action

Maps changed files to AWS accounts based on environment and file patterns.

```yaml
- name: Determine account number
  uses: ./.github/actions/account-mapping
  with:
    changed-files: ${{ steps.changes.outputs.files }}
    environment: ${{ steps.env.outputs.aft_account }}
```

### Changed Files Action

Detects changed files based on regex patterns.

```yaml
- name: Find changed files
  uses: ./.github/actions/changed-files
  with:
    pattern: |
      ^src/.*
      ^tests/.*
```

## Workflows

### Plan-Only CodePipeline

Triggers AWS CodePipeline for plan-only operations with environment-aware account routing.

```yaml
- name: Plan-Only CodePipeline Trigger
  uses: ./.github/workflows/plan-only-codepipeline.yml
```

## Development

### Adding New Hooks

1. Create your hook script in `hooks/`
2. Add it to `.pre-commit-config.yaml`
3. Install with `pre-commit install`

### Testing Hooks

```bash
# Run all hooks on staged files
pre-commit run

# Run specific hook
pre-commit run prepare-commit-msg

# Run on all files
pre-commit run --all-files
```

### Updating Hooks

```bash
# Update hook versions
pre-commit autoupdate

# Reinstall hooks
pre-commit install
```

## Configuration

### JIRA Hook Configuration

Edit `hooks/prepare-commit-msg` to customize:

- **JIRA Patterns**: Modify `JIRA_PATTERNS` array
- **Skip Prefixes**: Add to `SKIP_PREFIXES` array
- **Format**: Change `JIRA_PREFIX_FORMAT`

### Pre-commit Configuration

Edit `.pre-commit-config.yaml` to:

- Add/remove hooks
- Configure hook options
- Update hook versions

## Troubleshooting

### Hook Not Running

```bash
# Check if hooks are installed
ls -la .git/hooks/

# Reinstall hooks
pre-commit install --overwrite
```

### JIRA Ticket Not Detected

```bash
# Check branch name
git branch --show-current

# Test pattern manually
echo "feature/ABC-123-test" | grep -oE '[A-Z]+-[0-9]+'
```

### Pre-commit Errors

```bash
# Skip hooks for one commit
git commit --no-verify -m "emergency fix"

# Run hooks manually
pre-commit run --all-files
```

## Contributing

1. Create a feature branch with JIRA ticket: `feature/ABC-123-description`
2. Make your changes to dev
3. Commit with descriptive message (JIRA ticket will be auto-added)
4. Push and create a pull request

## License

MIT License - see LICENSE file for details.
