#!/usr/bin/env python3
"""
Configuration for HTML report generation.
"""

# Grip configuration
GRIP_CONFIG = {
    "title": "Report",
    "export_format": "html",
    "user_content": False,
    "wide": False,
    "clear_cache": False,
}

# HTML generation settings
HTML_SETTINGS = {
    "default_title": "Generated Report",
    "default_filename": "report",
    "file_extension": ".html",
    "temp_file_suffix": ".md",
    "temp_file_mode": "w",
}
