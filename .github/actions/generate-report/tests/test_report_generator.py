#!/usr/bin/env python3
"""
Unit tests for the report generator action.
Tests both JSON to PDF and Markdown to HTML conversion.
"""

import json
import os
import sys
import tempfile
import unittest

# Add parent directory to path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import after path setup
from generate_json_pdf import create_pdf_report  # noqa: E402
from generate_markdown_html import create_html_report  # noqa: E402


class TestReportGenerator(unittest.TestCase):
    """Test cases for report generation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample JSON data for testing
        self.sample_json = {
            "title": "Test Pipeline Report",
            "execution_details": {
                "start_time": "2024-01-15T10:30:00Z",
                "end_time": "2024-01-15T10:35:00Z",
                "duration": "5 minutes",
                "status": "success",
            },
            "commit_information": {
                "sha": "abc123def456",
                "message": "Add new feature",
                "author": "John Doe",
                "timestamp": "2024-01-15T10:25:00Z",
            },
            "quality_checks": {
                "linting": "passed",
                "security_scan": "passed",
                "coverage": "95.2%",
            },
            "test_results": [
                "Unit tests: 150/150 passed",
                "Integration tests: 25/25 passed",
                "E2E tests: 10/10 passed",
            ],
        }

        # Sample Markdown data for testing
        self.sample_markdown = """# Test Markdown Report

## Executive Summary

This is a **test report** generated from *Markdown* content using **Grip** for \
GitHub-style rendering.

## Test Results

| Test Type | Status | Count |
|-----------|--------|-------|
| Unit Tests | ✅ Passed | 150 |
| Integration Tests | ✅ Passed | 25 |
| E2E Tests | ✅ Passed | 10 |

## Code Quality

- **Coverage**: 95.2%
- **Linting**: Passed
- **Security Scan**: Passed
- **Performance**: Excellent

## Code Example

```python
def test_function():
    print("Hello, World!")
    return True
```

## Next Steps

1. Deploy to staging
2. Run smoke tests
3. Deploy to production
4. Monitor performance

---

*Report generated on 2024-01-15 using Grip*
"""

    def tearDown(self):
        """Clean up after tests."""
        # Clean up any generated files
        test_files = [
            "test-report.pdf",
            "test-report.html",
            "test-json-pdf.pdf",
            "test-markdown-html.html",
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_json_pdf_generation(self):
        """Test JSON to PDF conversion."""
        # Set up environment variables
        os.environ["REPORT_DATA"] = json.dumps(self.sample_json)
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        # Generate PDF
        report_path = create_pdf_report()

        # Assertions
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".pdf"))
        self.assertGreater(os.path.getsize(report_path), 0)

    def test_markdown_html_generation(self):
        """Test Markdown to HTML conversion."""
        # Set up environment variables
        os.environ["REPORT_DATA"] = self.sample_markdown
        os.environ["DATA_TYPE"] = "markdown"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        # Generate HTML
        report_path = create_html_report()

        # Assertions
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".html"))
        self.assertGreater(os.path.getsize(report_path), 0)

    def test_json_pdf_with_custom_filename(self):
        """Test JSON to PDF with custom filename."""
        # Set up environment variables
        os.environ["REPORT_DATA"] = json.dumps(self.sample_json)
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "test-json-pdf"

        # Generate PDF
        report_path = create_pdf_report()

        # Assertions
        self.assertEqual(report_path, "test-json-pdf.pdf")
        self.assertTrue(os.path.exists(report_path))

    def test_markdown_html_with_custom_filename(self):
        """Test Markdown to HTML with custom filename."""
        # Set up environment variables
        os.environ["REPORT_DATA"] = self.sample_markdown
        os.environ["DATA_TYPE"] = "markdown"
        os.environ["OUTPUT_FILENAME"] = "test-markdown-html"

        # Generate HTML
        report_path = create_html_report()

        # Assertions
        self.assertEqual(report_path, "test-markdown-html.html")
        self.assertTrue(os.path.exists(report_path))

    def test_json_pdf_empty_data(self):
        """Test JSON to PDF with empty data."""
        # Set up environment variables with empty data
        os.environ["REPORT_DATA"] = "{}"
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        # Generate PDF
        report_path = create_pdf_report()

        # Assertions
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".pdf"))

    def test_markdown_html_empty_data(self):
        """Test Markdown to HTML with empty data."""
        # Set up environment variables with empty data
        os.environ["REPORT_DATA"] = ""
        os.environ["DATA_TYPE"] = "markdown"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        # This should raise an exception for empty markdown
        with self.assertRaises(SystemExit):
            create_html_report()

    def test_json_pdf_invalid_json(self):
        """Test JSON to PDF with invalid JSON data."""
        # Set up environment variables with invalid JSON
        os.environ["REPORT_DATA"] = "{invalid json}"
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        # This should raise an exception for invalid JSON
        with self.assertRaises(SystemExit):
            create_pdf_report()

    def test_file_size_validation(self):
        """Test that generated files have reasonable sizes."""
        # Test JSON to PDF
        os.environ["REPORT_DATA"] = json.dumps(self.sample_json)
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        pdf_path = create_pdf_report()
        pdf_size = os.path.getsize(pdf_path)

        # PDF should be at least 1KB
        self.assertGreater(pdf_size, 1024)

        # Test Markdown to HTML
        os.environ["REPORT_DATA"] = self.sample_markdown
        os.environ["DATA_TYPE"] = "markdown"
        os.environ["OUTPUT_FILENAME"] = "test-report"

        html_path = create_html_report()
        html_size = os.path.getsize(html_path)

        # HTML should be at least 10KB (includes CSS)
        self.assertGreater(html_size, 10240)


class TestReportGeneratorIntegration(unittest.TestCase):
    """Integration tests for the report generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after tests."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_full_workflow_json(self):
        """Test complete JSON to PDF workflow."""
        sample_data = {
            "title": "Integration Test Report",
            "summary": "This is a test of the complete workflow",
            "results": {"status": "success", "tests": 42},
        }

        # Set up environment
        os.environ["REPORT_DATA"] = json.dumps(sample_data)
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "integration-test"

        # Generate report
        report_path = create_pdf_report()

        # Verify result
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".pdf"))

        # Clean up
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_full_workflow_markdown(self):
        """Test complete Markdown to HTML workflow."""
        sample_data = """# Integration Test

## Summary
This is a test of the complete workflow.

## Results
- Status: Success
- Tests: 42

## Code
```python
print("Hello, World!")
```
"""

        # Set up environment
        os.environ["REPORT_DATA"] = sample_data
        os.environ["DATA_TYPE"] = "markdown"
        os.environ["OUTPUT_FILENAME"] = "integration-test"

        # Generate report
        report_path = create_html_report()

        # Verify result
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".html"))

        # Clean up
        if os.path.exists(report_path):
            os.remove(report_path)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
