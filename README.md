# Cyan Actions

[![Test Custom Actions](https://github.com/chaunceyyann/cyan-actions/actions/workflows/test-custom-actions.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions/workflows/test-custom-actions.yml)
[![PR Checks](https://github.com/chaunceyyann/cyan-actions/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/chaunceyyann/cyan-actions/actions/workflows/pr-checks.yml)

A collection of shared GitHub Actions workflows, custom actions, and development tools for improved CI/CD automation.

## 📚 Documentation

- **[Custom Actions](.github/actions/README.md)** - Reusable composite actions
- **[Workflows](.github/workflows/README.md)** - Shared CI/CD workflows
- **[Git Hooks](hooks/README.md)** - Development workflow automation

## 🚀 Quick Start

### Using Shared Workflows

```yaml
# .github/workflows/your-workflow.yml
name: Use Shared Workflow
on:
  pull_request:
    branches: [main]
jobs:
  python-ci:
    uses: chaunceyyann/cyan-actions/.github/workflows/reusable-python-ci.yml@main
    with:
      python-version: '3.11'
      run-integration-tests: true
```

### Using Custom Actions

```yaml
# In your workflow steps
- name: Find changed files
  uses: chaunceyyann/cyan-actions/.github/actions/changed-files@main
  with:
    pattern: ".*\\.py$"
```

## 🧪 Testing

This repository includes comprehensive testing for all custom actions and workflows:

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test complete workflows and actions
- **Automated CI**: Tests run on every PR and push

See [.github/workflows/test-custom-actions.yml](.github/workflows/test-custom-actions.yml) for details.

## 🤝 Contributing

1. Create a feature branch: `feature/ABC-123-description`
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.
