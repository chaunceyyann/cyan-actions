#!/usr/bin/env python3
"""
PDF Styles Creation
"""

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from .config import COLORS, HEADING_STYLE_CONFIG, TITLE_STYLE_CONFIG


def create_styles():
    """Create custom paragraph styles."""
    base_styles = getSampleStyleSheet()

    return {
        "base_styles": base_styles,
        "title": ParagraphStyle(
            "CustomTitle",
            parent=base_styles["Heading1"],
            fontSize=TITLE_STYLE_CONFIG["font_size"],
            spaceAfter=TITLE_STYLE_CONFIG["space_after"],
            alignment=TITLE_STYLE_CONFIG["alignment"],
            textColor=COLORS["primary"],
            fontName="Helvetica-Bold",
            spaceBefore=TITLE_STYLE_CONFIG["space_before"],
        ),
        "heading": ParagraphStyle(
            "CustomHeading",
            parent=base_styles["Heading2"],
            fontSize=HEADING_STYLE_CONFIG["font_size"],
            spaceAfter=HEADING_STYLE_CONFIG["space_after"],
            spaceBefore=HEADING_STYLE_CONFIG["space_before"],
            textColor=COLORS["secondary"],
            fontName="Helvetica-Bold",
            leftIndent=0,
            alignment=TA_LEFT,
        ),
        "normal": ParagraphStyle(
            "CustomNormal",
            parent=base_styles["Normal"],
            fontSize=11,
            textColor=COLORS["text"],
            fontName="Helvetica",
            spaceAfter=8,
            leading=14,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base_styles["Normal"],
            fontSize=9,
            textColor=COLORS["border"],
            fontName="Helvetica",
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
    }
