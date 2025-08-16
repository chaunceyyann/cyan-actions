# Report Generator Action

This GitHub Action generates professional reports in both PDF and HTML formats from JSON or Markdown data.

## Features

- **PDF Generation**: Creates professional PDF reports using ReportLab
- **HTML Generation**: Generates GitHub-style HTML reports using Grip
- **Flexible Input**: Supports both JSON and Markdown data formats
- **Customizable**: Configurable styling and layout options

## Proposed Directory Structure

```
.github/actions/generate-report/
├── src/
│   ├── pdf/
│   │   ├── __init__.py
│   │   ├── generator.py          # Main PDF generator class
│   │   ├── config.py             # PDF configuration
│   │   ├── styles.py             # PDF styling
│   │   ├── utils.py              # PDF utilities
│   │   └── table_factory.py      # Table creation
│   ├── html/
│   │   ├── __init__.py
│   │   ├── generator.py          # Main HTML generator class
│   │   ├── config.py             # HTML configuration
│   │   └── utils.py              # HTML utilities
│   └── common/
│       ├── __init__.py
│       ├── logging.py            # Shared logging setup
│       └── utils.py              # Shared utilities
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_pdf_generator.py
│   │   └── test_html_generator.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_report_generation.py
│   └── fixtures/
│       ├── sample_data.json
│       └── sample_markdown.md
├── scripts/
│   ├── test_local.py             # Local testing script
│   └── generate_report.py        # Main entry point
├── action.yml                    # GitHub Action definition
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## Benefits of New Structure

### 1. **Clear Separation of Concerns**
- PDF and HTML generation are completely separate
- Each format has its own configuration and utilities
- Common functionality is shared through the `common` module

### 2. **Consistent Architecture**
- Both PDF and HTML generators follow similar patterns
- Object-oriented approach for both formats
- Consistent configuration and utility patterns

### 3. **Better Maintainability**
- Easy to add new report formats (e.g., DOCX, RTF)
- Clear module boundaries
- Easier to test individual components

### 4. **Improved Testing**
- Unit tests for each generator separately
- Integration tests for complete workflows
- Test fixtures for consistent test data

### 5. **Scalability**
- Easy to add new features to either format
- Clear import paths
- Modular design supports future extensions

## Current vs Proposed Structure

### Current Issues:
- Mixed architectural patterns (OOP vs functional)
- Inconsistent file naming
- Hard to extend with new formats
- Testing is scattered

### Proposed Benefits:
- Consistent object-oriented design
- Clear module organization
- Easy to maintain and extend
- Better test organization

## Migration Plan

1. **Phase 1**: Create new directory structure
2. **Phase 2**: Refactor HTML generator to match PDF generator pattern
3. **Phase 3**: Move existing files to new structure
4. **Phase 4**: Update imports and tests
5. **Phase 5**: Update documentation

## Usage

### PDF Generation
```python
from src.pdf.generator import PDFGenerator

generator = PDFGenerator(data, "output")
filename = generator.generate()
```

### HTML Generation
```python
from src.html.generator import HTMLGenerator

generator = HTMLGenerator(data, "output")
filename = generator.generate()
```

## Development

### Running Tests
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# All tests
python -m pytest tests/
```

### Local Testing
```bash
python scripts/test_local.py
```

## Dependencies

- **PDF Generation**: ReportLab
- **HTML Generation**: Grip
- **Testing**: pytest, unittest.mock
- **Development**: black, mypy
