#!/usr/bin/env python3
"""
HTML Report Generator using Grip.
Generates professional HTML reports from Markdown data with GitHub-style rendering.
"""

import os
import sys
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.logging import get_logger
from common.utils import validate_data

from .config import HTML_SETTINGS
from .utils import (
    cleanup_temp_file,
    create_temp_markdown_file,
    run_grip_command,
    validate_grip_installation,
)

logger = get_logger(__name__)


class HTMLGenerator:
    """Main HTML generator class that orchestrates the report creation."""

    def __init__(self, markdown_content: str, output_filename: str = "report"):
        """
        Initialize the HTML generator.

        Args:
            markdown_content: Markdown content to convert
            output_filename: Base filename for output (without extension)
        """
        self.markdown_content = markdown_content
        self.output_filename = f"{output_filename}{HTML_SETTINGS['file_extension']}"
        self.logger = logger

    def generate(self) -> str:
        """
        Generate the complete HTML report.

        Returns:
            str: Path to the generated HTML file

        Raises:
            RuntimeError: If Grip is not installed or generation fails
        """
        self.logger.info("Starting HTML report generation")

        # Validate Grip installation
        if not validate_grip_installation():
            raise RuntimeError("Grip is not installed or not available in PATH")

        # Validate input data
        validate_data(self.markdown_content, "markdown")

        # Generate HTML
        self.logger.info("Generating HTML with Grip...")
        filename = self._generate_html_with_grip()

        self.logger.info(f"HTML report generated successfully: {filename}")
        return filename

    def _generate_html_with_grip(self) -> str:
        """
        Generate HTML from Markdown using Grip.

        Returns:
            str: Path to the generated HTML file
        """
        temp_md_path = None

        try:
            # Create temporary markdown file
            temp_md_path = create_temp_markdown_file(self.markdown_content)

            # Run Grip command
            run_grip_command(
                temp_md_path,
                self.output_filename.replace(".html", ""),
                HTML_SETTINGS["default_title"],
            )

            return self.output_filename

        except Exception as e:
            self.logger.error(f"HTML generation failed: {e}")
            raise RuntimeError(f"Failed to generate HTML: {e}")

        finally:
            # Clean up temporary file
            if temp_md_path:
                cleanup_temp_file(temp_md_path)


def create_html_report() -> str:
    """
    Create an HTML report from Markdown data using Grip.
    This function maintains backward compatibility with the original interface.

    Returns:
        str: Path to the generated HTML file
    """
    from common.utils import get_environment_data, get_output_filename

    logger.info("Starting Markdown HTML report generation with Grip")

    # Get inputs from environment variables
    markdown_content = get_environment_data()
    output_filename = get_output_filename()

    logger.info(f"Output filename: {output_filename}")

    # Create generator and generate report
    generator = HTMLGenerator(markdown_content, output_filename)
    return generator.generate()


def main():
    """Main function to generate HTML report."""
    from common.logging import setup_logging
    from common.utils import exit_with_error, exit_with_success

    logger = setup_logging()

    try:
        logger.info("Starting Markdown HTML generation process")
        filename = create_html_report()
        exit_with_success(f"Successfully generated HTML: {filename}")
    except Exception as e:
        exit_with_error(f"Error generating HTML: {e}")


if __name__ == "__main__":
    main()
