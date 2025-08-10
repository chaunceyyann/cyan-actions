# Generate Report Action

A GitHub Action that generates professional reports from JSON or Markdown data.

## Features

- **Two Clear Flows**:
  - Flow 1: JSON → PDF (using ReportLab)
  - Flow 2: Markdown → HTML (using Grip)
- **Conditional Dependencies**: Only installs what's needed
- **Fast Setup**: ~50% faster than installing all dependencies
- **Clean Architecture**: Separate files for each format

## Usage

### JSON to PDF

```yaml
- name: Generate Report
  uses: ./.github/actions/generate-report
  with:
    data: |
      {
        "title": "Build Report",
        "results": {"passed": 42, "failed": 0},
        "coverage": "95.2%"
      }
    data-type: "json"
    output-filename: "build-report"
```

### Markdown to HTML

```yaml
- name: Generate Report
  uses: ./.github/actions/generate-report
  with:
    data: |
      # Pipeline Report
      ## Summary
      This pipeline **successfully** completed all stages.

      ## Test Results
      | Test Type | Status | Count |
      |-----------|--------|-------|
      | Unit Tests | ✅ Passed | 150 |
      | Integration Tests | ✅ Passed | 25 |
    data-type: "markdown"
    output-filename: "pipeline-report"
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `data` | Data string (JSON or Markdown) | Yes | - |
| `data-type` | Type of input data (`json` or `markdown`) | No | `json` |
| `output-filename` | Output filename (without extension) | No | `report` |

## Outputs

| Output | Description |
|--------|-------------|
| `report-path` | Path to generated file (`.pdf` for JSON, `.html` for Markdown) |

## Architecture

```
.github/actions/generate-report/
├── action.yml                    # Main action definition
├── generate_json_pdf.py          # JSON → PDF (ReportLab)
├── generate_markdown_html.py     # Markdown → HTML (Grip)
├── requirements.txt              # Runtime dependencies
├── test_local.py                 # Local testing script
├── README.md                    # This file
└── tests/                       # Test suite
    ├── __init__.py              # Package initialization
    ├── test_report_generator.py # Main test suite
    └── requirements-test.txt    # Testing dependencies
```

## Performance

- **JSON processing**: ~2s setup, ~2MB dependencies
- **Markdown processing**: ~5s setup, ~5MB dependencies
- **Conditional installation**: Only installs required packages

## Testing

The action includes comprehensive unit tests in the `tests/` directory and a local testing script.

### Running Tests

```bash
# Run local tests (PDF and HTML generation)
python test_local.py

# Run unit tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_report_generator.py

# Run with coverage report
python -m pytest tests/ --cov=.
```

### Test Structure

```
tests/
├── __init__.py                    # Package initialization
├── test_report_generator.py       # Main test suite
└── requirements-test.txt          # Testing dependencies
```

### Test Coverage

The test suite covers:
- JSON to PDF conversion
- Markdown to HTML conversion
- Custom filename handling
- Error handling (empty/invalid data)
- File size validation
- Integration workflows

### Local Testing

The `test_local.py` script provides a quick way to test both PDF and HTML generation locally:
- Tests JSON to PDF conversion with sample data
- Tests Markdown to HTML conversion using the repository README
- Provides visual feedback on test results

## Dependencies

- **JSON**: ReportLab (lightweight PDF generation)
- **Markdown**: Grip (GitHub-style HTML rendering)

The action automatically installs only the dependencies needed for the specified data type using inline dependency management in the action.yml file.

### Requirements Files

- `requirements.txt` - Runtime dependencies for the action
- `tests/requirements-test.txt` - Testing dependencies (includes runtime deps)
