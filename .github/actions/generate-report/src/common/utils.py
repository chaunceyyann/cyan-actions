#!/usr/bin/env python3
"""
Shared utilities for report generators.
"""

import json
import os
import sys
from typing import Any, Dict, Union


def get_environment_data() -> str:
    """Get report data from environment variables."""
    return os.environ.get("REPORT_DATA", "")


def get_output_filename() -> str:
    """Get output filename from environment variables."""
    return os.environ.get("OUTPUT_FILENAME", "report")


def get_data_type() -> str:
    """Get data type from environment variables."""
    return os.environ.get("DATA_TYPE", "json")


def parse_json_data(data: str) -> Dict[str, Any]:
    """Parse JSON data with error handling."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {e}")


def validate_data(data: str, data_type: str) -> None:
    """Validate input data based on type."""
    if not data.strip():
        raise ValueError(f"No {data_type} content provided")

    if data_type == "json":
        try:
            parse_json_data(data)
        except ValueError as e:
            raise ValueError(f"Invalid JSON data: {e}")


def exit_with_error(message: str, exit_code: int = 1) -> None:
    """Exit with error message."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def exit_with_success(message: str) -> None:
    """Exit with success message."""
    print(f"Success: {message}")
    sys.exit(0)
