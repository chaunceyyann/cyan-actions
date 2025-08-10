#!/usr/bin/env python3
"""
Markdown HTML Report Generator using Grip.
Generates professional HTML reports from Markdown data with GitHub-style rendering.
"""

import logging
import os
import subprocess
import sys
import tempfile


def setup_logging():
    """Setup logging with GitHub Actions format."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


def generate_html_with_grip(markdown_content, output_filename):
    """Generate HTML from Markdown using Grip."""
    logger = logging.getLogger(__name__)

    # Create temporary markdown file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as temp_md:
        temp_md.write(markdown_content)
        temp_md_path = temp_md.name

    try:
        # Use Grip to convert Markdown to HTML
        # Grip exports to HTML file (not PDF)
        cmd = [
            "grip",
            temp_md_path,
            "--export",
            f"{output_filename}.html",
            "--title",
            output_filename,
        ]

        logger.info(f"Running Grip command: {' '.join(cmd)}")

        subprocess.run(cmd, capture_output=True, text=True, check=True)

        logger.info("Grip HTML generation completed successfully")
        return f"{output_filename}.html"

    except subprocess.CalledProcessError as e:
        logger.error(f"Grip failed: {e}")
        logger.error(f"Grip stdout: {e.stdout}")
        logger.error(f"Grip stderr: {e.stderr}")
        raise
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_md_path)
        except OSError:
            pass


def create_html_report():
    """Create an HTML report from Markdown data using Grip."""
    logger = logging.getLogger(__name__)
    logger.info("Starting Markdown HTML report generation with Grip")

    # Get inputs from environment variables
    markdown_content = os.environ.get("REPORT_DATA", "")
    output_filename = os.environ.get("OUTPUT_FILENAME", "report")

    logger.info(f"Output filename: {output_filename}")

    if not markdown_content.strip():
        logger.error("No Markdown content provided")
        sys.exit(1)

    # Generate HTML using Grip
    logger.info("Generating HTML with Grip...")
    filename = generate_html_with_grip(markdown_content, output_filename)

    logger.info(f"HTML report generated successfully: {filename}")
    return filename


def main():
    """Main function to generate HTML report."""
    logger = setup_logging()

    try:
        logger.info("Starting Markdown HTML generation process")
        filename = create_html_report()
        logger.info(f"Successfully generated HTML: {filename}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error generating HTML: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
