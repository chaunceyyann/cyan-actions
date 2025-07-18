# Git Hooks

This directory contains Git hooks for automated development workflow improvements.

## 📋 Available Hooks

### [commit-msg](commit-msg)

Automatically adds JIRA ticket numbers to commit messages based on branch names.

**Features:**
- Extracts JIRA tickets from branch names
- Supports multiple JIRA patterns
- Skips merge commits and special prefixes
- Provides clear feedback on operation

**Supported JIRA Patterns:**
- `JIRA-123` (standard format)
- `ABC123` (no dash format, auto-converts to `ABC-123`)
- `AB-123` (minimum 2 letters)

**Branch Naming Examples:**
| Branch Name | JIRA Ticket | Commit Message Result |
|-------------|-------------|----------------------|
| `feature/ABC-123-add-login` | ABC-123 | `[ABC-123] your message` |
| `bugfix/PROJECT-456-fix-bug` | PROJECT-456 | `[PROJECT-456] your message` |
| `hotfix/ABC789-critical-fix` | ABC-789 | `[ABC-789] your message` |
| `feature/ABC123-description` | ABC-123 | `[ABC-123] your message` |

**Installation:**
```bash
# Copy the hook to your repository
cp hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg
```

**Configuration:**
Edit the hook to customize:
- **JIRA Patterns**: Modify `JIRA_PATTERNS` array
- **Skip Prefixes**: Add to `SKIP_PREFIXES` array
- **Format**: Change `JIRA_PREFIX_FORMAT`

## 🔧 Pre-commit Configuration

This repository includes a comprehensive pre-commit configuration (`.pre-commit-config.yaml`) with:

### Available Hooks

- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with newline
- **check-yaml**: Validates YAML syntax
- **check-added-large-files**: Prevents large files from being committed
- **shellcheck**: Lints shell scripts for errors and best practices

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Or with Homebrew (macOS)
brew install pre-commit

# Install the hooks
pre-commit install

# Install the prepare-commit-msg hook specifically
pre-commit install --hook-type prepare-commit-msg
```

### Verification

```bash
# Check installed hooks
pre-commit run --all-files

# Test the commit-msg hook
git commit --allow-empty -m "test commit"
```

## 🔄 Git Hook Execution Order

```bash
git commit
├── 1. pre-commit hooks run
├── 2. prepare-commit-msg hook runs
├── 3. Git opens editor with commit message
├── 4. User edits message and saves/closes editor
├── 5. commit-msg hook runs ← This is where we modify
└── 6. Git creates the commit
```

**Why we use `commit-msg`**: This hook runs after the editor closes but before the commit is created, ensuring the JIRA ticket is reliably added regardless of how you commit.

## 🚫 Skipped Commits

The commit-msg hook automatically skips:
- Merge commits
- Revert commits
- Commits starting with: `Merge`, `Revert`, `WIP`, `Draft`

## 🧪 Testing

### Manual Testing

```bash
# Create a test branch with JIRA ticket
git checkout -b feature/ABC-123-test-hook

# Make a commit
git commit --allow-empty -m "test commit message"

# Should see: ✅ Added JIRA ticket [ABC-123] to commit message from branch: feature/ABC-123-test-hook
```

### Testing Hooks

```bash
# Run all hooks on staged files
pre-commit run

# Run specific hook
pre-commit run prepare-commit-msg

# Run on all files
pre-commit run --all-files
```

## 🔧 Development

### Adding New Hooks

1. Create your hook script in `hooks/`
2. Add it to `.pre-commit-config.yaml`
3. Install with `pre-commit install`

### Updating Hooks

```bash
# Update hook versions
pre-commit autoupdate

# Reinstall hooks
pre-commit install
```

### Customizing Pre-commit Configuration

Edit `.pre-commit-config.yaml` to:
- Add/remove hooks
- Configure hook options
- Update hook versions
- Set file patterns for specific hooks

## 🛠️ Troubleshooting

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

### Hook Configuration Issues

```bash
# Check pre-commit configuration
pre-commit run --all-files --verbose

# Update to latest versions
pre-commit autoupdate

# Clean and reinstall
pre-commit clean
pre-commit install
```

## 📁 Hook Structure

```
hooks/
├── commit-msg              # JIRA ticket automation
├── prepare-commit-msg      # Pre-commit hook (if needed)
└── README.md              # This documentation

.pre-commit-config.yaml    # Pre-commit configuration
```

## 🔗 Integration with CI/CD

These hooks integrate seamlessly with the CI/CD workflows:

- **Pre-commit checks** are enforced in pull requests
- **JIRA ticket format** is validated in commit messages
- **Code quality** is maintained through automated checks

## 📚 Related Documentation

- [Custom Actions](../.github/actions/README.md) - Actions that can be used in workflows
- [Workflows](../.github/workflows/README.md) - CI/CD workflows that use these hooks
