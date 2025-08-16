#!/usr/bin/env python3
"""
Class-based PDF Report Generator using ReportLab.
"""

import json
import logging
import os
import sys
from datetime import datetime

from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from .config import DOC_CONFIG
from .styles import create_styles
from .table_factory import TableFactory
from .utils import capitalize_header_text


class PDFGenerator:
    """Main PDF generator class that orchestrates the report creation."""

    def __init__(self, report_data, output_filename="report"):
        self.report_data = report_data
        self.output_filename = f"{output_filename}.pdf"
        self.styles = create_styles()
        self.table_factory = TableFactory(self.styles)
        self.logger = logging.getLogger(__name__)

    def generate(self):
        """Generate the complete PDF report."""
        self.logger.info("Starting PDF report generation")

        # Create document
        doc = self._create_document()

        # Build story
        story = self._build_story()

        # Build PDF
        self.logger.info("Building PDF document...")
        doc.build(story)
        self.logger.info(f"PDF report generated successfully: {self.output_filename}")
        return self.output_filename

    def _create_document(self):
        """Create the PDF document template."""
        return SimpleDocTemplate(
            self.output_filename,
            pagesize=DOC_CONFIG["page_size"],
            rightMargin=DOC_CONFIG["margins"],
            leftMargin=DOC_CONFIG["margins"],
            topMargin=DOC_CONFIG["margins"],
            bottomMargin=DOC_CONFIG["margins"],
        )

    def _build_story(self):
        """Build the complete story for the PDF."""
        story = []

        # Add title
        story.extend(self._create_title_section())

        # Add content sections
        story.extend(self._create_content_sections())

        # Add footer
        story.extend(self._create_footer_section())

        return story

    def _create_title_section(self):
        """Create title section."""
        story = []

        title = self.report_data.get("title", "Report")
        story.append(Paragraph(title, self.styles["title"]))
        story.append(Spacer(1, 15))

        # Add divider
        divider = self.table_factory.create_title_divider()
        story.append(divider)
        story.append(Spacer(1, 10))

        return story

    def _create_content_sections(self):
        """Create all content sections."""
        story = []

        for section_name, section_data in self.report_data.items():
            if section_name == "title":
                continue

            if isinstance(section_data, dict):
                story.extend(self._create_dict_section(section_name, section_data))
            elif isinstance(section_data, list):
                story.extend(self._create_list_section(section_name, section_data))
            else:
                story.extend(self._create_simple_section(section_name, section_data))

        return story

    def _create_dict_section(self, section_name, section_data):
        """Create a section for dictionary data."""
        story = []

        # Check if should use merged cells (for found_lines)
        should_use_merged_cells = any(
            isinstance(value, list) and len(value) > 1
            for value in section_data.values()
        )

        # Special handling for found_lines - always use merged table
        if section_name == "quality_check" and "found_lines" in section_data:
            table = self.table_factory.create_merged_table(section_data)
        elif should_use_merged_cells:
            table = self.table_factory.create_merged_table(section_data)
        else:
            table = self.table_factory.create_dict_table(section_data)

        if table:
            story.append(
                Paragraph(capitalize_header_text(section_name), self.styles["heading"])
            )
            story.append(table)
            story.append(Spacer(1, 8))

        return story

    def _create_list_section(self, section_name, section_data):
        """Create a section for list data."""
        story = []

        if not section_data:
            return story

        story.append(
            Paragraph(capitalize_header_text(section_name), self.styles["heading"])
        )

        # Check if list of objects with same structure (traditional table)
        if self._is_traditional_table_candidate(section_data):
            table = self.table_factory.create_traditional_table(section_data)
        else:
            table = self.table_factory.create_list_table(section_data, section_name)

        if table:
            story.append(table)
            story.append(Spacer(1, 8))

        return story

    def _is_traditional_table_candidate(self, section_data):
        """Check if list data should use traditional table format."""
        return (
            len(section_data) > 0
            and all(isinstance(item, dict) for item in section_data)
            and len(set(tuple(sorted(item.keys())) for item in section_data)) == 1
        )

    def _create_simple_section(self, section_name, section_data):
        """Create a section for simple string/number values."""
        story = []

        story.append(
            Paragraph(capitalize_header_text(section_name), self.styles["heading"])
        )

        value_text = str(section_data)
        if len(value_text) > 100:
            story.append(Paragraph(value_text, self.styles["normal"]))
        else:
            value_box = self.table_factory.create_value_box(value_text)
            story.append(value_box)

        story.append(Spacer(1, 8))
        return story

    def _create_footer_section(self):
        """Create footer section with timestamp."""
        story = []

        story.append(Spacer(1, 30))

        # Footer divider
        footer_divider = self.table_factory.create_footer_divider()
        story.append(footer_divider)

        # Timestamp in US Eastern timezone
        from .utils import get_current_time_eastern

        timestamp = get_current_time_eastern()
        story.append(Paragraph(timestamp, self.styles["footer"]))

        return story


def create_pdf_report():
    """Create a PDF report from JSON data using the class-based generator."""
    logger = logging.getLogger(__name__)
    logger.info("Starting JSON PDF report generation")

    # Parse input data
    report_data = _parse_report_data()
    output_filename = os.environ.get("OUTPUT_FILENAME", "report")

    # Create and run generator
    generator = PDFGenerator(report_data, output_filename)
    return generator.generate()


def _parse_report_data():
    """Parse JSON data from environment variables."""
    report_data_str = os.environ.get("REPORT_DATA", "{}")
    try:
        report_data = json.loads(report_data_str)
        logging.getLogger(__name__).debug(f"Parsed report data: {report_data}")
        return report_data
    except json.JSONDecodeError as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to parse REPORT_DATA: {e}")
        logger.error(f"Raw data: {report_data_str}")
        sys.exit(1)


def main():
    """Main function to generate PDF report."""
    logger = setup_logging()

    try:
        logger.info("Starting JSON PDF generation process")
        filename = create_pdf_report()
        logger.info(f"Successfully generated PDF: {filename}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        sys.exit(1)


def setup_logging():
    """Setup logging with GitHub Actions format."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


if __name__ == "__main__":
    main()
