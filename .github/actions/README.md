# Custom Actions

[![Test Custom Actions](https://github.com/chaunceyyann/cyan-actions/actions/workflows/test-custom-actions.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions/workflows/test-custom-actions.yml)
[![PR Checks](https://github.com/chaunceyyann/cyan-actions/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions/workflows/pr-checks.yml)

This directory contains reusable composite actions for common CI/CD tasks.

## 📋 Available Actions

### [changed-files](changed-files/)

Detects files that have changed in a pull request or push event, with optional pattern filtering.

**Usage:**
```yaml
- name: Find changed Python files
  uses: chaunceyyann/cyan-actions/.github/actions/changed-files@v0.1
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
  uses: chaunceyyann/cyan-actions/.github/actions/account-mapping@v0.1
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

### [check-keywords](check-keywords/)

Checks if git diff additions contain specific keywords or patterns.

**Usage:**
```yaml
- name: Check for sensitive keywords
  uses: chaunceyyann/cyan-actions/.github/actions/check-keywords@v0.1
  with:
    patterns: "secret_key,password,api_key,token"
    base-ref: "origin/dev"
```

**Inputs:**
- `patterns`: Comma-separated list of keywords/patterns to check
- `base-ref`: Base reference for git diff (default: "origin/dev")

**Outputs:**
- `found`: Boolean indicating if any patterns were found

**Features:**
- Checks only additions in git diff
- Configurable pattern matching
- Simple boolean output
- Efficient keyword scanning

### [check-codepipeline](check-codepipeline/)

Monitors AWS CodePipeline execution status with polling and detailed information retrieval.

**Usage:**
```yaml
- name: Check Pipeline Status
  uses: chaunceyyann/cyan-actions/.github/actions/check-codepipeline@v0.1
  with:
    execution-id: "abc123"
    pipeline-name: "my-pipeline"
    timeout-minutes: "30"
    aws-region: "us-west-2"
```

**Inputs:**
- `execution-id`: CodePipeline execution ID
- `pipeline-name`: Name of the CodePipeline
- `timeout-minutes`: Timeout in minutes (default: "30")
- `aws-region`: AWS region (default: "us-west-2")

**Outputs:**
- `status`: Pipeline execution status
- `start-time`: Pipeline start time
- `variables`: Pipeline variables (JSON)

**Features:**
- Polling with configurable timeout
- Detailed error handling and logging
- Retrieves pipeline metadata
- Comprehensive status reporting

### [generate-pdf-report](generate-pdf-report/)

Generates professional PDF reports using Python's reportlab library.

**Usage:**
```yaml
- name: Generate PDF Report
  uses: chaunceyyann/cyan-actions/.github/actions/generate-pdf-report@v0.1
  with:
    report-title: "Execution Report"
    generated-time: "2024-01-01T00:00:00Z"
    workflow-name: "My Workflow"
    run-id: "123456789"
    output-filename: "my-report"
```

**Inputs:**
- `report-title`: Title of the report
- `generated-time`: Timestamp when report was generated
- `workflow-name`: Name of the workflow
- `run-id`: GitHub run ID
- `pr-number`: Pull request number (optional)
- `pr-title`: Pull request title (optional)
- `execution-details`: JSON string with execution details
- `commit-information`: JSON string with commit information
- `quality-check`: JSON string with quality check results
- `pipeline-status`: JSON string with pipeline status
- `variables`: JSON string with variables (optional)
- `output-filename`: Base filename for the PDF

**Outputs:**
- `pdf-path`: Path to the generated PDF file

**Features:**
- Professional PDF formatting
- Configurable report sections
- JSON data integration
- Automatic artifact generation

### [run-codepipeline](run-codepipeline/)

Triggers AWS CodePipeline execution with environment-aware account routing.

**Usage:**
```yaml
- name: Trigger CodePipeline
  uses: chaunceyyann/cyan-actions/.github/actions/run-codepipeline@v0.1
  with:
    aws-region: "us-west-2"
    aws-target-account: "123456789012"
    aws-pipeline-account: "dev_account_number"
    commit-sha: ${{ github.sha }}
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Inputs:**
- `aws-region`: AWS region
- `aws-target-account`: Target AWS account number
- `aws-pipeline-account`: Pipeline account identifier
- `commit-sha`: Git commit SHA
- `aws-access-key-id`: AWS access key ID
- `aws-secret-access-key`: AWS secret access key

**Outputs:**
- `execution-id`: CodePipeline execution ID

**Features:**
- Environment-aware account routing
- Secure credential handling
- Execution tracking
- Error handling and logging

### [test-actions](test-actions/)

Tests custom actions for syntax errors and basic functionality.

**Usage:**
```yaml
- name: Test Custom Actions
  uses: chaunceyyann/cyan-actions/.github/actions/test-actions@v0.1
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
  uses: chaunceyyann/cyan-actions/.github/actions/test-workflows@v0.1
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
