#!/usr/bin/env python3
"""
PDF Configuration and Styling Constants
"""

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# =============================================================================
# COLOR SCHEME
# =============================================================================

COLORS = {
    "primary": HexColor("#2E86AB"),  # Professional blue
    "secondary": HexColor("#A23B72"),  # Purple accent
    "accent": HexColor("#F18F01"),  # Orange accent
    "text": HexColor("#2C3E50"),  # Dark blue-grey text
    "light_bg": HexColor("#F8F9FA"),  # Light background
    "header_bg": HexColor("#2E86AB"),  # Header background
    "header_text": HexColor("#F0F0F0"),  # Header text color
    "row_light": HexColor("#F8F9FA"),  # Light row background
    "row_dark": HexColor("#E9ECEF"),  # Dark row background
    "border": HexColor("#DEE2E6"),  # Border color
}

# =============================================================================
# TABLE CONFIGURATION
# =============================================================================

TABLE_CONFIG = {
    "header_font": "Helvetica-Bold",
    "header_font_size": 11,
    "value_font": "Helvetica",
    "value_font_size": 10,
    "border_width": 0.5,
    "padding": {
        "header": {"top": 8, "bottom": 8, "left": 12, "right": 12},
        "value": {"top": 8, "bottom": 8, "left": 12, "right": 12},
    },
    "cell_styles": {
        "header": {
            "text_color": "header_text",
            "font_name": "header_font",
            "font_size": "header_font_size",
            "alignment": TA_LEFT,
            "background_color": "header_bg",
        },
        "value": {
            "text_color": "text",
            "font_name": "value_font",
            "font_size": "value_font_size",
            "alignment": TA_LEFT,
            "background_color": None,
        },
    },
}

# =============================================================================
# DOCUMENT CONFIGURATION
# =============================================================================

DOC_CONFIG = {
    "page_size": A4,
    "margins": 36,
    "total_width": 6.0 * inch,
    "min_header_width": 1.2 * inch,
    "max_header_width": 3.0 * inch,
    "header_char_width": 0.08,
    "header_padding": 0.3 * inch,
}

# =============================================================================
# STYLE CONFIGURATION
# =============================================================================

TITLE_STYLE_CONFIG = {
    "font_size": 20,
    "space_after": 20,
    "space_before": 15,
    "alignment": TA_CENTER,
}

HEADING_STYLE_CONFIG = {
    "font_size": 14,
    "space_after": 10,
    "space_before": 15,
}
