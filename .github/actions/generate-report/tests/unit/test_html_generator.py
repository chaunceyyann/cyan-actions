#!/usr/bin/env python3
"""
Unit tests for HTML generator.
Tests individual components with proper mocking.
"""

import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path to import the modules
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import after path setup
from src.html_generator.run import HTMLGenerator  # noqa: E402


class TestMarkdownHTMLUnit(unittest.TestCase):
    """Unit tests for Markdown to HTML conversion with proper mocking."""

    def setUp(self):
        """Set up test fixtures."""
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

    @patch("src.html_generator.run.run_grip_command")
    @patch("src.html_generator.run.create_temp_markdown_file")
    @patch("src.html_generator.run.validate_grip_installation")
    @patch("src.html_generator.run.validate_data")
    def test_generate_html_with_grip_success(
        self, mock_validate_data, mock_validate_grip, mock_create_temp, mock_run_grip
    ):
        """Test successful HTML generation with Grip."""
        # Mock validations
        mock_validate_grip.return_value = True
        mock_validate_data.return_value = None

        # Mock temporary file creation
        mock_create_temp.return_value = "/tmp/test.md"

        # Mock grip command success
        mock_run_grip.return_value = None

        generator = HTMLGenerator(self.sample_markdown, "test-report")
        result = generator.generate()

        self.assertEqual(result, "test-report.html")
        mock_create_temp.assert_called_once_with(self.sample_markdown)
        mock_run_grip.assert_called_once()

    @patch("src.html_generator.run.run_grip_command")
    @patch("src.html_generator.run.create_temp_markdown_file")
    @patch("src.html_generator.run.validate_grip_installation")
    @patch("src.html_generator.run.validate_data")
    def test_generate_html_with_grip_failure(
        self, mock_validate_data, mock_validate_grip, mock_create_temp, mock_run_grip
    ):
        """Test HTML generation failure with Grip."""
        # Mock validations
        mock_validate_grip.return_value = True
        mock_validate_data.return_value = None

        # Mock temporary file creation
        mock_create_temp.return_value = "/tmp/test.md"

        # Mock grip command failure
        mock_run_grip.side_effect = RuntimeError("Grip command failed")

        generator = HTMLGenerator(self.sample_markdown, "test-report")

        with self.assertRaises(RuntimeError):
            generator.generate()

    @patch("src.html_generator.run.validate_grip_installation")
    @patch("src.html_generator.run.validate_data")
    def test_generate_with_grip_not_installed(
        self, mock_validate_data, mock_validate_grip
    ):
        """Test HTML generation when Grip is not installed."""
        mock_validate_data.return_value = None
        mock_validate_grip.return_value = False

        generator = HTMLGenerator(self.sample_markdown, "test-report")

        with self.assertRaises(RuntimeError) as context:
            generator.generate()

        self.assertIn("Grip is not installed", str(context.exception))

    @patch("src.html_generator.run.validate_grip_installation")
    @patch("src.html_generator.run.run_grip_command")
    @patch("src.html_generator.run.create_temp_markdown_file")
    @patch("src.html_generator.run.validate_data")
    def test_generate_success(
        self, mock_validate_data, mock_create_temp, mock_run_grip, mock_validate_grip
    ):
        """Test successful HTML generation."""
        mock_validate_data.return_value = None
        mock_validate_grip.return_value = True

        # Mock temporary file creation
        mock_create_temp.return_value = "/tmp/test.md"

        # Mock grip command success
        mock_run_grip.return_value = None

        generator = HTMLGenerator(self.sample_markdown, "test-report")
        result = generator.generate()

        self.assertEqual(result, "test-report.html")

    def test_html_generator_initialization(self):
        """Test HTMLGenerator initialization."""
        generator = HTMLGenerator(self.sample_markdown, "test-report")

        self.assertEqual(generator.markdown_content, self.sample_markdown)
        self.assertEqual(generator.output_filename, "test-report.html")

    @patch("src.html_generator.run.validate_grip_installation")
    @patch("src.html_generator.run.run_grip_command")
    @patch("src.html_generator.run.create_temp_markdown_file")
    @patch("src.html_generator.run.validate_data")
    def test_html_generator_with_empty_content(
        self, mock_validate_data, mock_create_temp, mock_run_grip, mock_validate_grip
    ):
        """Test HTMLGenerator with empty content."""
        mock_validate_data.side_effect = ValueError("Empty content")
        mock_validate_grip.return_value = True
        mock_create_temp.return_value = "/tmp/test.md"
        mock_run_grip.return_value = None

        generator = HTMLGenerator("", "test-report")

        with self.assertRaises(ValueError):
            generator.generate()

    @patch("src.html_generator.run.validate_grip_installation")
    @patch("src.html_generator.run.run_grip_command")
    @patch("src.html_generator.run.create_temp_markdown_file")
    @patch("src.html_generator.run.validate_data")
    def test_html_generator_with_whitespace_only_content(
        self, mock_validate_data, mock_create_temp, mock_run_grip, mock_validate_grip
    ):
        """Test HTMLGenerator with whitespace-only content."""
        mock_validate_data.side_effect = ValueError("Whitespace only content")
        mock_validate_grip.return_value = True
        mock_create_temp.return_value = "/tmp/test.md"
        mock_run_grip.return_value = None

        generator = HTMLGenerator("   \n\t   ", "test-report")

        with self.assertRaises(ValueError):
            generator.generate()


if __name__ == "__main__":
    unittest.main(verbosity=2)
