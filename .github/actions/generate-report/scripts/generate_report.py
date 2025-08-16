#!/usr/bin/env python3
"""
Main entry point for report generation.
Supports both PDF and HTML generation from JSON or Markdown data.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from common.logging import setup_logging
from common.utils import (
    exit_with_error,
    exit_with_success,
    get_data_type,
    get_environment_data,
    get_output_filename,
)


def main():
    """Main function to generate reports based on data type."""
    logger = setup_logging()

    try:
        # Get inputs
        data = get_environment_data()
        output_filename = get_output_filename()
        data_type = get_data_type()

        logger.info(
            f"Starting report generation - Type: {data_type}, Output: {output_filename}"
        )

        if data_type == "json":
            # Generate PDF from JSON
            from common.utils import parse_json_data
            from pdf_generator.run import PDFGenerator

            json_data = parse_json_data(data)
            generator = PDFGenerator(json_data, output_filename)
            filename = generator.generate()

        elif data_type == "markdown":
            # Generate HTML from Markdown
            from html_generator.run import HTMLGenerator

            generator = HTMLGenerator(data, output_filename)
            filename = generator.generate()

        else:
            exit_with_error(f"Unsupported data type: {data_type}")

        exit_with_success(f"Successfully generated report: {filename}")

    except Exception as e:
        exit_with_error(f"Error generating report: {e}")


if __name__ == "__main__":
    main()
