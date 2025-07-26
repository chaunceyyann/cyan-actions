# Git Hooks

[![Test Custom Actions](https://github.com/chaunceyyann/cyan-actions/actions/workflows/test-custom-actions.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions/workflows/test-custom-actions.yml)
[![PR Checks](https://github.com/chaunceyyann/cyan-actions/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions/workflows/pr-checks.yml)

This directory contains custom Git hooks for automated development workflows.

## Available Hooks

### JIRA Commit Message Hook

Automatically prepends JIRA ticket numbers from branch names to commit messages.

#### Usage with Pre-commit

1. **Add to your `.pre-commit-config.yaml`:**
   ```yaml
   # Use the shared JIRA commit-msg.sh hook
   - repo: https://github.com/chaunceyyann/cyan-actions
     rev: dev  # or a specific tag/commit
     hooks:
       - id: jira-commit-msg
   ```
   > **Note:** Remove any previous `repo: local` block for `commit-msg` to avoid conflicts.

2. **Install the commit-msg hook:**
   ```bash
   pre-commit install --hook-type commit-msg
   ```

#### Manual Installation

If you prefer to install the hook manually:

1. **Copy the hook to your repository:**
   ```bash
   cp hooks/commit-msg.sh .git/hooks/commit-msg
   chmod +x .git/hooks/commit-msg
   ```

2. **Or install via pre-commit:**
   ```bash
   # Install the prepare-commit-msg hook specifically
   pre-commit install --hook-type prepare-commit-msg
   ```

#### How It Works

The hook runs during the commit process:

1. **Branch name detection**: Extracts JIRA ticket from branch name
2. **Pattern matching**: Supports standard and custom JIRA patterns
3. **Message modification**: Prepends ticket to commit message
4. **Validation**: Skips merge commits, reverts, WIP, and Draft commits

#### Git Commit Flow

```
git commit
├── 1. Editor opens
├── 2. prepare-commit-msg hook runs
├── 3. User writes message
├── 4. Editor closes
├── 5. commit-msg hook runs ← This is where we modify
└── 6. Commit is created
```

**Why we use `commit-msg`**: This hook runs after the editor closes but before the commit is created, ensuring the JIRA ticket is reliably added regardless of how you commit.

#### Supported Patterns

The commit-msg.sh hook automatically skips:
- **Merge commits**: `Merge branch 'feature/ABC-123'`
- **Revert commits**: `Revert "ABC-123: Add feature"`
- **WIP commits**: `WIP: Add feature`
- **Draft commits**: `Draft: Add feature`

#### JIRA Ticket Patterns

- **Standard**: `ABC-123`, `PROJ-456`
- **Custom**: Configurable via environment variables
- **Branch formats**:
  - `feature/ABC-123-description`
  - `bugfix/PROJ-456-fix-issue`
  - `hotfix/ABC-789-urgent-fix`

#### Testing

Test the hook locally:

```bash
# Test pre-commit hooks
pre-commit run prepare-commit-msg

# Test the commit-msg hook
git checkout -b feature/ABC-123-test
git commit --allow-empty -m 'test commit'
# Should result: [ABC-123] test commit
```

#### Troubleshooting

**Hook not running:**
- Ensure hook is executable: `chmod +x .git/hooks/commit-msg`
- Check pre-commit installation: `pre-commit install --hook-type commit-msg`

**JIRA ticket not added:**
- Verify branch name contains valid JIRA pattern
- Check hook logs for error messages
- Ensure hook is properly installed

**Pre-commit conflicts:**
- Remove any local `commit-msg` hook configurations
- Use only the shared hook from this repository

## Hook Files

```
hooks/
├── commit-msg.sh              # JIRA ticket automation
└── prepare-commit-msg         # Pre-commit hook (if needed)
```

## Configuration

### Environment Variables

- `JIRA_PATTERN`: Custom regex pattern for JIRA tickets (default: `[A-Z]+-\d+`)
- `SKIP_PATTERNS`: Patterns to skip (default: merge, revert, WIP, Draft)

### Pre-commit Configuration

The hook integrates seamlessly with pre-commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/chaunceyyann/cyan-actions
    rev: dev
    hooks:
      - id: jira-commit-msg
```

## Contributing

When modifying hooks:

1. **Test locally** before committing
2. **Update documentation** for any changes
3. **Version appropriately** for shared usage
4. **Follow Git hook best practices**

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
