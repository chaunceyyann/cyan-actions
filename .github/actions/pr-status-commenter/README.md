# PR Status Commenter Action

Automatically post comments on Pull Requests when checks pass or fail. This action monitors check runs and posts appropriate comments to provide feedback to PR authors and reviewers.

## Features

- ✅ **Automatic commenting** on PR success/failure
- 🚫 **Duplicate prevention** to avoid spam
- 🔗 **Check result links** for easy navigation
- 🎨 **Customizable templates** with variable support
- 📊 **Check monitoring** for specific required checks
- 🤖 **Configurable bot name** for comment signatures

## Usage

### Basic Usage

```yaml
- name: Comment on PR Status
  uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
```

### Advanced Usage

```yaml
- name: Comment on PR Status
  uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
  with:
    required-checks: 'pre-commit,terraform-lint,security-scan'
    prevent-duplicates: 'true'
    include-check-links: 'true'
    bot-name: 'My Custom Bot'
    success-template: |
      🎉 **All checks passed!**

      Great work! The following checks completed successfully:
      {{checks}}

      Ready for review! 🚀
    failure-template: |
      ❌ **Checks failed**

      Please fix the following issues:
      {{checks}}

      [View details](https://github.com/{{repo}}/pull/{{pr_number}}/checks)
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `required-checks` | Comma-separated list of required checks to monitor | No | `pre-commit,terraform-lint` |
| `success-template` | Success comment template with variable support | No | See default template below |
| `failure-template` | Failure comment template with variable support | No | See default template below |
| `prevent-duplicates` | Prevent duplicate comments (true/false) | No | `true` |
| `include-check-links` | Include links to check results (true/false) | No | `true` |
| `bot-name` | Bot name for comment signatures | No | `PR Status Commenter` |
| `check-suite-id` | Check suite ID to monitor (auto-detected if not provided) | No | `""` |

## Outputs

| Output | Description |
|--------|-------------|
| `commented` | Whether a comment was posted (true/false) |
| `comment-type` | Type of comment posted (success/failure/none) |

## Template Variables

Both success and failure templates support the following variables:

- `{{checks}}` - List of checks with their status (✅/❌)
- `{{pr_number}}` - PR number
- `{{repo}}` - Repository name (owner/repo)
- `{{bot_name}}` - Bot name for signatures

## Default Templates

### Success Template
```
✅ **All PR checks passed successfully!**

🎉 Great job! All automated checks have completed successfully:
{{checks}}

This PR is ready for review! 🚀

📋 **Check Results:**
- [View all checks](https://github.com/{{repo}}/pull/{{pr_number}}/checks)

*This comment was automatically posted by the PR Status Commenter.*
```

### Failure Template
```
❌ **Some PR checks failed**

Please review the failed checks and fix any issues before requesting a review.

📋 **Check Results:**
- [View all checks](https://github.com/{{repo}}/pull/{{pr_number}}/checks)

*This comment was automatically posted by the PR Status Commenter.*
```

## Examples

### Monitor Specific Checks
```yaml
- name: Comment on PR Status
  uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
  with:
    required-checks: 'lint,test,build,security'
```

### Custom Success Message
```yaml
- name: Comment on PR Status
  uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
  with:
    success-template: |
      🚀 **Deployment Ready!**

      All checks passed successfully:
      {{checks}}

      This PR is approved for deployment! 🎯
```

### Disable Check Links
```yaml
- name: Comment on PR Status
  uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
  with:
    include-check-links: 'false'
```

### Allow Duplicate Comments
```yaml
- name: Comment on PR Status
  uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
  with:
    prevent-duplicates: 'false'
```

## Workflow Integration

### Trigger on Check Completion
```yaml
name: PR Status Commenter

on:
  check_suite:
    types: [completed]
  check_run:
    types: [completed]

permissions:
  issues: write
  pull-requests: write
  checks: read
  contents: read

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - name: Comment on PR Status
        uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
```

### Use in Existing Workflow
```yaml
jobs:
  my-checks:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test

      - name: Comment on PR Status
        uses: chaunceyyann/cyan-actions/.github/actions/pr-status-commenter@main
        if: always()
```

## Requirements

- **Permissions**: The workflow using this action must have:
  - `issues: write` - To post comments on PRs
  - `pull-requests: write` - To read PR information
  - `checks: read` - To read check run status
  - `contents: read` - To read repository content

## Troubleshooting

### No Comments Posted
- Check that the workflow has the required permissions
- Verify that the required checks are actually running
- Ensure the action is triggered on the correct events

### Duplicate Comments
- Set `prevent-duplicates: 'true'` to avoid duplicate comments
- The action checks for existing comments before posting

### Custom Templates Not Working
- Ensure template variables use double curly braces: `{{variable}}`
- Check that the template is properly formatted in YAML

## Contributing

This action is part of the `cyan-actions` collection. Contributions are welcome!

## License

This action is licensed under the same license as the `cyan-actions` repository.
