#!/usr/bin/env python3
"""
Unit tests for PDF generator.
Tests individual components with proper mocking.
"""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path to import the modules
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import after path setup
from src.pdf_generator.run import PDFGenerator  # noqa: E402


class TestPDFGeneratorUnit(unittest.TestCase):
    """Unit tests for PDFGenerator class with proper mocking."""

    def setUp(self):
        """Set up test fixtures."""
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

    @patch("src.pdf_generator.run.SimpleDocTemplate")
    @patch("src.pdf_generator.run.create_styles")
    @patch("src.pdf_generator.run.TableFactory")
    def test_pdf_generator_initialization(
        self, mock_table_factory, mock_create_styles, mock_doc_template
    ):
        """Test PDFGenerator initialization."""
        mock_styles = {
            "title": MagicMock(),
            "normal": MagicMock(),
            "heading": MagicMock(),
            "footer": MagicMock(),
        }
        mock_create_styles.return_value = mock_styles

        generator = PDFGenerator(self.sample_json, "test-report")

        self.assertEqual(generator.report_data, self.sample_json)
        self.assertEqual(generator.output_filename, "test-report.pdf")
        self.assertEqual(generator.styles, mock_styles)
        mock_table_factory.assert_called_once_with(mock_styles)

    @patch("src.pdf_generator.run.SimpleDocTemplate")
    @patch("src.pdf_generator.run.create_styles")
    @patch("src.pdf_generator.run.TableFactory")
    def test_pdf_generator_create_document(
        self, mock_table_factory, mock_create_styles, mock_doc_template
    ):
        """Test document creation."""
        mock_styles = {
            "title": MagicMock(),
            "normal": MagicMock(),
            "heading": MagicMock(),
            "footer": MagicMock(),
        }
        mock_create_styles.return_value = mock_styles
        mock_doc_instance = MagicMock()
        mock_doc_template.return_value = mock_doc_instance

        generator = PDFGenerator(self.sample_json, "test-report")
        result = generator._create_document()

        mock_doc_template.assert_called_once()
        self.assertEqual(result, mock_doc_instance)

    @patch("src.pdf_generator.run.SimpleDocTemplate")
    @patch("src.pdf_generator.run.create_styles")
    @patch("src.pdf_generator.run.TableFactory")
    @patch("src.pdf_generator.run.Paragraph")
    @patch("src.pdf_generator.run.Spacer")
    def test_pdf_generator_build_story(
        self,
        mock_spacer,
        mock_paragraph,
        mock_table_factory,
        mock_create_styles,
        mock_doc_template,
    ):
        """Test story building."""
        mock_styles = {
            "title": MagicMock(),
            "normal": MagicMock(),
            "heading": MagicMock(),
            "footer": MagicMock(),
        }
        mock_create_styles.return_value = mock_styles
        mock_table_factory_instance = MagicMock()
        mock_table_factory.return_value = mock_table_factory_instance
        mock_table_factory_instance.create_title_divider.return_value = MagicMock()

        # Mock Paragraph and Spacer to avoid ReportLab font issues
        mock_paragraph.return_value = MagicMock()
        mock_spacer.return_value = MagicMock()

        generator = PDFGenerator(self.sample_json, "test-report")
        story = generator._build_story()

        # Story should contain elements (title, content sections, footer)
        self.assertIsInstance(story, list)
        self.assertGreater(len(story), 0)

    @patch("src.pdf_generator.run.SimpleDocTemplate")
    @patch("src.pdf_generator.run.create_styles")
    @patch("src.pdf_generator.run.TableFactory")
    @patch("src.pdf_generator.run.Paragraph")
    @patch("src.pdf_generator.run.Spacer")
    def test_pdf_generator_title_section(
        self,
        mock_spacer,
        mock_paragraph,
        mock_table_factory,
        mock_create_styles,
        mock_doc_template,
    ):
        """Test title section creation."""
        mock_styles = {
            "title": MagicMock(),
            "normal": MagicMock(),
            "heading": MagicMock(),
            "footer": MagicMock(),
        }
        mock_create_styles.return_value = mock_styles
        mock_table_factory_instance = MagicMock()
        mock_table_factory.return_value = mock_table_factory_instance
        mock_table_factory_instance.create_title_divider.return_value = MagicMock()

        # Mock Paragraph and Spacer to avoid ReportLab font issues
        mock_paragraph.return_value = MagicMock()
        mock_spacer.return_value = MagicMock()

        generator = PDFGenerator(self.sample_json, "test-report")
        title_section = generator._create_title_section()

        self.assertIsInstance(title_section, list)
        self.assertGreater(len(title_section), 0)

    @patch("src.pdf_generator.run.SimpleDocTemplate")
    @patch("src.pdf_generator.run.create_styles")
    @patch("src.pdf_generator.run.TableFactory")
    @patch("src.pdf_generator.run.Paragraph")
    def test_pdf_generator_content_sections(
        self, mock_paragraph, mock_table_factory, mock_create_styles, mock_doc_template
    ):
        """Test content sections creation."""
        mock_styles = {
            "title": MagicMock(),
            "normal": MagicMock(),
            "heading": MagicMock(),
            "footer": MagicMock(),
        }
        mock_create_styles.return_value = mock_styles
        mock_table_factory_instance = MagicMock()
        mock_table_factory.return_value = mock_table_factory_instance

        # Mock Paragraph to avoid ReportLab font issues
        mock_paragraph.return_value = MagicMock()

        generator = PDFGenerator(self.sample_json, "test-report")
        content_sections = generator._create_content_sections()

        self.assertIsInstance(content_sections, list)

    @patch("src.pdf_generator.run.SimpleDocTemplate")
    @patch("src.pdf_generator.run.create_styles")
    @patch("src.pdf_generator.run.TableFactory")
    @patch("src.pdf_generator.run.Paragraph")
    @patch("src.pdf_generator.run.Spacer")
    def test_pdf_generator_generate_method(
        self,
        mock_spacer,
        mock_paragraph,
        mock_table_factory,
        mock_create_styles,
        mock_doc_template,
    ):
        """Test the main generate method."""
        mock_styles = {
            "title": MagicMock(),
            "normal": MagicMock(),
            "heading": MagicMock(),
            "footer": MagicMock(),
        }
        mock_create_styles.return_value = mock_styles
        mock_table_factory_instance = MagicMock()
        mock_table_factory.return_value = mock_table_factory_instance
        mock_table_factory_instance.create_title_divider.return_value = MagicMock()

        # Mock Paragraph and Spacer to avoid ReportLab font issues
        mock_paragraph.return_value = MagicMock()
        mock_spacer.return_value = MagicMock()

        mock_doc_instance = MagicMock()
        mock_doc_template.return_value = mock_doc_instance

        generator = PDFGenerator(self.sample_json, "test-report")
        result = generator.generate()

        self.assertEqual(result, "test-report.pdf")
        mock_doc_instance.build.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
