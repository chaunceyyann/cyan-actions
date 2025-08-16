#!/usr/bin/env python3
"""
Utilities for HTML report generation.
"""

import os
import subprocess
import sys
import tempfile
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.logging import get_logger

logger = get_logger(__name__)


def create_temp_markdown_file(content: str) -> str:
    """Create a temporary markdown file with the given content."""
    temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
    temp_file.write(content)
    temp_file.close()
    return temp_file.name


def cleanup_temp_file(file_path: str) -> None:
    """Clean up a temporary file."""
    try:
        os.unlink(file_path)
    except OSError:
        logger.warning(f"Could not remove temporary file: {file_path}")


def run_grip_command(markdown_file: str, output_filename: str, title: str) -> None:
    """Run the Grip command to convert markdown to HTML."""
    cmd = [
        "grip",
        markdown_file,
        "--export",
        f"{output_filename}.html",
        "--title",
        title,
    ]

    logger.info(f"Running Grip command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    logger.info("Grip HTML generation completed successfully")


def validate_grip_installation() -> bool:
    """Check if Grip is installed and available."""
    try:
        subprocess.run(["grip", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
