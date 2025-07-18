# Custom Actions

This directory contains reusable composite actions for common CI/CD tasks.

## 📋 Available Actions

### [changed-files](changed-files/)

Detects files that have changed in a pull request or push event, with optional pattern filtering.

**Usage:**
```yaml
- name: Find changed Python files
  uses: ./.github/actions/changed-files
  with:
    pattern: ".*\\.py$"
```

**Inputs:**
- `pattern` (optional): Regex pattern to filter changed files

**Outputs:**
- `files`: Space-separated list of changed files

**Features:**
- Works with both pull requests and push events
- Handles edge cases like missing merge base
- Provides detailed logging for debugging
- Graceful fallback when git operations fail

### [account-mapping](account-mapping/)

Maps changed files to AWS account numbers based on environment and file patterns.

**Usage:**
```yaml
- name: Determine account number
  uses: ./.github/actions/account-mapping
  with:
    changed-files: ${{ steps.changes.outputs.files }}
    environment: "dev"
```

**Inputs:**
- `changed-files`: Space-separated list of changed files
- `environment`: Target environment (dev, prod, etc.)

**Outputs:**
- `account_number`: Comma-separated list of account numbers

**Features:**
- Environment-aware account routing
- Supports multiple file types (src, tests, etc.)
- Configurable via `mappings.yml`
- Comprehensive error handling

### [test-actions](test-actions/)

Tests custom actions for syntax errors and basic functionality.

**Usage:**
```yaml
- name: Test Custom Actions
  uses: ./.github/actions/test-actions
```

**Features:**
- Validates action.yml syntax
- Checks for required fields
- Tests shell script syntax
- Validates Dockerfile syntax
- Tests JavaScript actions with npm

### [test-workflows](test-workflows/)

Tests reusable workflows for syntax errors and configuration.

**Usage:**
```yaml
- name: Test Reusable Workflows
  uses: ./.github/actions/test-workflows
```

**Features:**
- Validates workflow.yml syntax
- Checks for required inputs/outputs
- Tests workflow structure
- Validates job configurations

## 🧪 Testing

Each action includes comprehensive tests:

### Unit Tests
- Test individual functions and components
- Mock external dependencies
- Validate input/output handling

### Integration Tests
- Test complete action execution
- Validate real-world scenarios
- Test error conditions

### Running Tests
```bash
# Run all tests for an action
cd .github/actions/action-name
python -m pytest tests/ -v

# Run specific test types
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

## 📁 Action Structure

Each action follows this structure:
```
action-name/
├── action.yml          # Action definition
├── requirements.txt    # Python dependencies (if needed)
├── main.py            # Main logic (if needed)
├── tests/             # Test directory
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
└── README.md          # Action-specific documentation
```

## 🔧 Development

### Creating a New Action

1. Create a new directory in `.github/actions/`
2. Add `action.yml` with proper inputs/outputs
3. Implement the action logic
4. Add comprehensive tests
5. Update this README

### Action Best Practices

- **Use composite actions** for simple shell-based actions
- **Use Docker actions** for complex dependencies
- **Include comprehensive tests** for all actions
- **Provide clear documentation** with examples
- **Handle errors gracefully** with meaningful messages
- **Use semantic versioning** for releases

### Testing Your Action

```bash
# Test action syntax
yamllint action.yml

# Test with sample inputs
# (Create a test workflow to validate)

# Run integration tests
python -m pytest tests/integration/ -v
```

## 📚 Related Documentation

- [Workflows](../workflows/README.md) - How to use these actions in workflows
- [Git Hooks](../../hooks/README.md) - Development workflow automation
