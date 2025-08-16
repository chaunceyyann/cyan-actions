#!/usr/bin/env python3
"""
Integration tests for report generation.
Tests complete workflows and file generation.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

# Add parent directory to path to import the modules
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from src.html_generator.run import HTMLGenerator, create_html_report  # noqa: E402

# Import after path setup
from src.pdf_generator.run import PDFGenerator, create_pdf_report  # noqa: E402


class TestReportGeneratorIntegration(unittest.TestCase):
    """Integration tests for the report generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_json = {
            "title": "Integration Test Report",
            "summary": "This is a test of the complete workflow",
            "results": {"status": "success", "tests": 42},
        }
        self.sample_markdown = """# Integration Test

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

    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)

        # Clean up any generated files
        test_files = [
            "test-report.pdf",
            "test-report.html",
            "test-json-pdf.pdf",
            "test-markdown-html.html",
            "integration-test.pdf",
            "integration-test.html",
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_full_workflow_json(self):
        """Test complete JSON to PDF workflow."""
        # Set up environment
        os.environ["REPORT_DATA"] = json.dumps(self.sample_json)
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "integration-test"

        # Generate report
        report_path = create_pdf_report()

        # Verify result
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".pdf"))

    def test_full_workflow_markdown(self):
        """Test complete Markdown to HTML workflow."""
        # Set up environment
        os.environ["REPORT_DATA"] = self.sample_markdown
        os.environ["DATA_TYPE"] = "markdown"
        os.environ["OUTPUT_FILENAME"] = "integration-test"

        # Generate report
        report_path = create_html_report()

        # Verify result
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".html"))

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
        with self.assertRaises(ValueError):
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


class TestLocalPDFValidation(unittest.TestCase):
    """Test class for local PDF validation - kept for manual PDF inspection."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_json = {
            "title": "Test Report - Table Styles Comparison",
            "basic_info": {
                "project": "Test Project very loooooooooooooooooooooooong name that should test how the PDF generator handles extremely long text in table cells and whether it wraps properly or gets cut off",
                "version": "1.0.0",
                "created": "2024-01-15 10:30:00",
                "status": "Active",
            },
            "activities": [
                "Code review completed",
                "Tests passed",
                "Deployment successful",
            ],
            "team_members": [
                {
                    "name": "John Doe",
                    "role": "Developer",
                    "email": "john.doe@example.com",
                },
                {
                    "name": "Jane Smith",
                    "role": "QA Engineer",
                    "email": "jane.smith@example.com",
                },
                {
                    "name": "Bob Wilson",
                    "role": "DevOps",
                    "email": "bob.wilson@example.com",
                },
                {
                    "name": "Alice Johnson",
                    "role": "Senior Software Engineer with very loooooooooooooooooooooooong title that should test text wrapping",
                    "email": "alice.johnson@example.com",
                },
            ],
            "notes": "This is a test report generated locally.",
        }

    def test_local_pdf_generation(self):
        """Test local PDF generation for manual validation.
        This test creates a PDF file that can be manually inspected.
        """
        # Set up environment variables
        os.environ["REPORT_DATA"] = json.dumps(self.sample_json)
        os.environ["DATA_TYPE"] = "json"
        os.environ["OUTPUT_FILENAME"] = "test_local_validation"

        # Generate PDF
        report_path = create_pdf_report()

        # Assertions
        self.assertTrue(os.path.exists(report_path))
        self.assertTrue(report_path.endswith(".pdf"))
        self.assertGreater(os.path.getsize(report_path), 0)

        print(f"\n✅ Local PDF validation file created: {report_path}")
        print(
            "   You can manually inspect this file to validate PDF generation quality."
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
