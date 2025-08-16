#!/usr/bin/env python3
"""
PDF Utilities - Common functions for PDF generation
"""

import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle

from .config import COLORS, TABLE_CONFIG


def format_timestamp(timestamp_str, timezone="US/Eastern"):
    """Format timestamp to US Eastern timezone with pretty format."""
    if not timestamp_str:
        return ""

    try:
        # Parse the ISO timestamp
        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

        # Convert to US Eastern timezone
        eastern_tz = ZoneInfo(timezone)
        eastern_time = dt.astimezone(eastern_tz)

        # Format as "Jan 15, 2024 at 10:30 AM EST"
        return eastern_time.strftime("%b %d, %Y at %I:%M %p %Z")
    except Exception as e:
        logging.getLogger(__name__).warning(
            f"Failed to format timestamp '{timestamp_str}': {e}"
        )
        return timestamp_str


def format_value(value):
    """Format a value for display, handling timestamps and other special cases."""
    if isinstance(value, str):
        # Check if it looks like a timestamp
        if any(keyword in value.lower() for keyword in ["time", "date", "timestamp"]):
            return format_timestamp(value)
        return value
    elif isinstance(value, (dict, list)):
        return json.dumps(value, indent=2)
    else:
        return str(value)


def create_cell_style_from_config(styles, cell_type):
    """Create a cell style from the centralized configuration."""
    if cell_type not in TABLE_CONFIG["cell_styles"]:
        raise ValueError(f"Unknown cell type: {cell_type}")

    cell_config = TABLE_CONFIG["cell_styles"][cell_type]
    return ParagraphStyle(
        f"{cell_type.title()}Cell",
        parent=styles["Normal"],
        textColor=COLORS[cell_config["text_color"]],
        alignment=cell_config["alignment"],
        fontName=TABLE_CONFIG[cell_config["font_name"]],
        fontSize=TABLE_CONFIG[cell_config["font_size"]],
    )


def create_header_cell_style(styles):
    """Create custom style for table header cells."""
    return create_cell_style_from_config(styles, "header")


def create_value_cell_style(styles):
    """Create custom style for table value cells."""
    return create_cell_style_from_config(styles, "value")


def get_current_time_eastern():
    """Get current time in US Eastern timezone."""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    # Get current time in UTC
    utc_now = datetime.now(ZoneInfo("UTC"))

    # Convert to US Eastern timezone
    eastern_tz = ZoneInfo("US/Eastern")
    eastern_time = utc_now.astimezone(eastern_tz)

    # Format as "Generated on January 15, 2024 at 10:30 AM EST"
    return eastern_time.strftime("Generated on %B %d, %Y at %I:%M %p %Z")


def capitalize_header_text(text):
    """Convert snake_case to Title Case for headers."""
    return text.replace("_", " ").title()
