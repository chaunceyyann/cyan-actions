#!/usr/bin/env python3
"""
JSON PDF Report Generator using ReportLab.
Generates professional PDF reports from JSON data.
"""

import json
import logging
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# =============================================================================
# CONFIGURATION - Colors and Styling
# =============================================================================

# Color Scheme
# This defines the color palette used throughout the PDF report.
# The header color issue was resolved by ensuring header cells use COLORS['header_text']
# instead of the default black color, providing proper contrast against the header
# background.
COLORS = {
    "primary": HexColor("#2E86AB"),  # Professional blue
    "secondary": HexColor("#A23B72"),  # Purple accent
    "accent": HexColor("#F18F01"),  # Orange accent
    "text": HexColor("#2C3E50"),  # Dark blue-grey text
    "light_bg": HexColor("#F8F9FA"),  # Light background
    "header_bg": HexColor("#2E86AB"),  # Header background (professional blue)
    "header_text": HexColor("#F0F0F0"),  # Header text color (light grey for contrast)
    "row_light": HexColor("#F8F9FA"),  # Light row background
    "row_dark": HexColor("#E9ECEF"),  # Dark row background
    "border": HexColor("#DEE2E6"),  # Border color
}

# Table Configuration
# This section defines all table-related styling, including the cell style
# configuration that was introduced to fix the header color issue. The
# cell_styles configuration centralizes all cell styling options, making it
# easier to maintain consistency and modify styles across the entire document.
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
    # Cell Style Configuration - Centralized styling for table cells
    # This configuration was introduced to fix the header color issue by
    # ensuring that header cells use the correct text color
    # (COLORS['header_text']) instead of the default black color. The
    # configuration references other TABLE_CONFIG values and COLORS to
    # maintain consistency and avoid hardcoding.
    "cell_styles": {
        "header": {
            "text_color": "header_text",  # References COLORS['header_text']
            "font_name": "header_font",  # References TABLE_CONFIG['header_font']
            "font_size": "header_font_size",  # References TABLE_CONFIG
            "alignment": TA_LEFT,
            "background_color": "header_bg",  # References COLORS['header_bg']
        },
        "value": {
            "text_color": "text",  # References COLORS['text']
            "font_name": "value_font",  # References TABLE_CONFIG['value_font']
            "font_size": "value_font_size",  # References TABLE_CONFIG
            "alignment": TA_LEFT,
            "background_color": None,  # No specific background, uses alternating rows
        },
    },
}

# Document Configuration
DOC_CONFIG = {
    "page_size": A4,
    "margins": 36,  # Reduced from 72
    "total_width": 6.0 * inch,  # 6 inches total width
    "min_header_width": 1.2 * inch,
    "max_header_width": 3.0 * inch,
    "header_char_width": 0.08,  # Inches per character for header width calculation
    "header_padding": 0.3 * inch,
}

# Title and Heading Styles
TITLE_STYLE_CONFIG = {
    "font_size": 20,  # Reduced from 24
    "space_after": 20,  # Reduced from 30
    "space_before": 15,  # Reduced from 20
    "alignment": TA_CENTER,
}

HEADING_STYLE_CONFIG = {
    "font_size": 14,  # Reduced from 16
    "space_after": 10,  # Reduced from 15
    "space_before": 15,  # Reduced from 25
}


def setup_logging():
    """Setup logging with GitHub Actions format."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


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
    """Create a cell style from the centralized configuration.

    Args:
        styles: The base styles from ReportLab
        cell_type: Either 'header' or 'value'

    Returns:
        ParagraphStyle: Configured style for the cell type
    """
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
    """Create custom style for table header cells using centralized configuration."""
    return create_cell_style_from_config(styles, "header")


def create_value_cell_style(styles):
    """Create custom style for table value cells using centralized configuration."""
    return create_cell_style_from_config(styles, "value")


def create_table_from_dict(data, title, styles, header_width=None, value_width=None):
    """Create a table from a dictionary with enhanced styling."""
    if not data:
        return None

    # Create custom styles for this table
    header_cell_style = create_header_cell_style(styles)
    value_cell_style = create_value_cell_style(styles)

    # Format the data for display with proper text wrapping
    formatted_data = []

    for k, v in data.items():
        formatted_value = format_value(v)
        # Create capitalized header text
        header_text = k.replace("_", " ").title()

        # Create Paragraph objects for text wrapping with capitalized headers
        key_para = Paragraph(header_text, header_cell_style)
        value_para = Paragraph(str(formatted_value), value_cell_style)
        formatted_data.append([key_para, value_para])

    if not formatted_data:
        return None

    # Use provided widths or calculate default
    if header_width is None or value_width is None:
        # Calculate dynamic column widths based on header length
        max_key_length = max(len(k.replace("_", " ").title()) for k in data.keys())
        header_width = max(
            DOC_CONFIG["min_header_width"],
            max_key_length * DOC_CONFIG["header_char_width"]
            + DOC_CONFIG["header_padding"],
        )
        value_width = DOC_CONFIG["total_width"] - header_width

    # Create table with column widths
    table = Table(formatted_data, colWidths=[header_width, value_width])

    # Get padding values
    header_pad = TABLE_CONFIG["padding"]["header"]
    value_pad = TABLE_CONFIG["padding"]["value"]

    table.setStyle(
        TableStyle(
            [
                # First column (keys) styling as headers
                ("BACKGROUND", (0, 0), (0, -1), COLORS["header_bg"]),
                ("TEXTCOLOR", (0, 0), (0, -1), COLORS["header_text"]),
                ("FONTNAME", (0, 0), (0, -1), TABLE_CONFIG["header_font"]),
                ("FONTSIZE", (0, 0), (0, -1), TABLE_CONFIG["header_font_size"]),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("VALIGN", (0, 0), (0, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (0, -1), header_pad["bottom"]),
                ("TOPPADDING", (0, 0), (0, -1), header_pad["top"]),
                ("LEFTPADDING", (0, 0), (0, -1), header_pad["left"]),
                ("RIGHTPADDING", (0, 0), (0, -1), header_pad["right"]),
                # Second column (values) styling
                ("TEXTCOLOR", (1, 0), (1, -1), colors.black),
                ("FONTNAME", (1, 0), (1, -1), TABLE_CONFIG["value_font"]),
                ("FONTSIZE", (1, 0), (1, -1), TABLE_CONFIG["value_font_size"]),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (1, 0), (1, -1), "TOP"),
                ("BOTTOMPADDING", (1, 0), (1, -1), value_pad["bottom"]),
                ("TOPPADDING", (1, 0), (1, -1), value_pad["top"]),
                ("LEFTPADDING", (1, 0), (1, -1), value_pad["left"]),
                ("RIGHTPADDING", (1, 0), (1, -1), value_pad["right"]),
                # Borders - default width
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    TABLE_CONFIG["border_width"],
                    COLORS["border"],
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (0, -1),
                    TABLE_CONFIG["border_width"],
                    COLORS["border"],
                ),
                # Alternating row backgrounds for the value column
                (
                    "ROWBACKGROUNDS",
                    (1, 0),
                    (1, -1),
                    [COLORS["row_light"], COLORS["row_dark"]],
                ),
            ]
        )
    )

    return table


def create_pdf_report():
    """Create a PDF report from JSON data using ReportLab."""
    logger = logging.getLogger(__name__)
    logger.info("Starting JSON PDF report generation with ReportLab")

    # Get inputs from environment variables
    report_data_str = os.environ.get("REPORT_DATA", "{}")
    output_filename = os.environ.get("OUTPUT_FILENAME", "report")

    logger.info(f"Output filename: {output_filename}")

    # Parse JSON data
    try:
        report_data = json.loads(report_data_str)
        logger.debug(f"Parsed report data: {report_data}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse REPORT_DATA: {e}")
        logger.error(f"Raw data: {report_data_str}")
        sys.exit(1)

    # Create PDF document
    filename = f"{output_filename}.pdf"
    logger.info(f"Creating PDF document: {filename}")

    doc = SimpleDocTemplate(
        filename,
        pagesize=DOC_CONFIG["page_size"],
        rightMargin=DOC_CONFIG["margins"],
        leftMargin=DOC_CONFIG["margins"],
        topMargin=DOC_CONFIG["margins"],
        bottomMargin=DOC_CONFIG["margins"],
    )

    # Get styles and create custom styles
    styles = getSampleStyleSheet()

    # Enhanced title style
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=TITLE_STYLE_CONFIG["font_size"],
        spaceAfter=TITLE_STYLE_CONFIG["space_after"],
        alignment=TITLE_STYLE_CONFIG["alignment"],
        textColor=COLORS["primary"],
        fontName="Helvetica-Bold",
        spaceBefore=TITLE_STYLE_CONFIG["space_before"],
    )

    # Enhanced heading style
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=HEADING_STYLE_CONFIG["font_size"],
        spaceAfter=HEADING_STYLE_CONFIG["space_after"],
        spaceBefore=HEADING_STYLE_CONFIG["space_before"],
        textColor=COLORS["secondary"],
        fontName="Helvetica-Bold",
        leftIndent=0,
        alignment=TA_LEFT,
    )

    # Enhanced normal text style
    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=11,
        textColor=COLORS["text"],
        fontName="Helvetica",
        spaceAfter=8,
        leading=14,
    )

    # Custom style for table header cells
    header_cell_style = create_header_cell_style(styles)

    # Custom style for table value cells
    value_cell_style = create_value_cell_style(styles)

    # Build story
    story = []

    # Title with enhanced styling
    title = report_data.get("title", "Report")
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 15))  # Reduced from 30

    # Add a subtle divider line
    divider = Table(
        [[""]], colWidths=[DOC_CONFIG["total_width"]], rowHeights=[1]
    )  # Reduced from 2
    divider.setStyle(
        TableStyle(
            [
                ("LINEABOVE", (0, 0), (-1, 0), 1, COLORS["primary"]),
                ("BACKGROUND", (0, 0), (-1, 0), COLORS["light_bg"]),
            ]
        )
    )
    story.append(divider)
    story.append(Spacer(1, 10))  # Reduced from 20

    # First pass: calculate maximum header length across all sections
    max_header_length = 0

    for section_name, section_data in report_data.items():
        if section_name == "title":
            continue

        if isinstance(section_data, dict):
            # Check dictionary keys
            for k in section_data.keys():
                header_text = k.replace("_", " ").title()
                max_header_length = max(max_header_length, len(header_text))
        elif isinstance(section_data, list):
            # Check list section names
            section_header = section_name.replace("_", " ").title()
            max_header_length = max(
                max_header_length, len(section_header) + 3
            )  # +3 for " 1", " 2", etc.

    # Calculate consistent header width for all tables
    header_width = max(1.2, max_header_length * 0.08 + 0.3) * inch
    value_width = 6.0 * inch - header_width

    # Second pass: create tables with consistent header width
    for section_name, section_data in report_data.items():
        if section_name == "title":
            continue  # Skip title as it's already handled

        if isinstance(section_data, dict):
            # Create a table for dictionary data
            table = create_table_from_dict(
                section_data, section_name, styles, header_width, value_width
            )
            if table:
                story.append(
                    Paragraph(section_name.replace("_", " ").title(), heading_style)
                )
                story.append(table)
                story.append(Spacer(1, 8))  # Reduced from 15
        elif isinstance(section_data, list):
            # Handle list data with enhanced styling
            if section_data:
                story.append(
                    Paragraph(section_name.replace("_", " ").title(), heading_style)
                )

                # Check if this is a list of objects with the same structure
                # (traditional table)
                if (
                    len(section_data) > 0
                    and all(isinstance(item, dict) for item in section_data)
                    and len(set(tuple(sorted(item.keys())) for item in section_data))
                    == 1
                ):

                    # Traditional table style - headers at top
                    all_keys = list(section_data[0].keys())
                    # Create header row with Paragraph objects and capitalized headers
                    header_row = [
                        Paragraph(key.replace("_", " ").title(), header_cell_style)
                        for key in all_keys
                    ]
                    list_data = [header_row]

                    for item in section_data:
                        # Create data row with Paragraph objects for text wrapping
                        row = [
                            Paragraph(
                                str(format_value(item.get(key, ""))), value_cell_style
                            )
                            for key in all_keys
                        ]
                        list_data.append(row)

                    # Calculate column widths based on number of columns
                    num_cols = len(all_keys)
                    col_width = DOC_CONFIG["total_width"] / num_cols
                    col_widths = [col_width] * num_cols

                    table = Table(list_data, colWidths=col_widths)

                    # Traditional table styling
                    header_pad = TABLE_CONFIG["padding"][
                        "value"
                    ]  # Use value padding for traditional tables

                    table.setStyle(
                        TableStyle(
                            [
                                # Header row styling
                                ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
                                ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["header_text"]),
                                (
                                    "FONTNAME",
                                    (0, 0),
                                    (-1, 0),
                                    TABLE_CONFIG["header_font"],
                                ),
                                (
                                    "FONTSIZE",
                                    (0, 0),
                                    (-1, 0),
                                    TABLE_CONFIG["header_font_size"],
                                ),
                                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                                ("VALIGN", (0, 0), (-1, 0), "TOP"),
                                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                                ("TOPPADDING", (0, 0), (-1, 0), 12),
                                # Data rows styling
                                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                                (
                                    "FONTNAME",
                                    (0, 1),
                                    (-1, -1),
                                    TABLE_CONFIG["value_font"],
                                ),
                                (
                                    "FONTSIZE",
                                    (0, 1),
                                    (-1, -1),
                                    TABLE_CONFIG["value_font_size"],
                                ),
                                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                                (
                                    "BOTTOMPADDING",
                                    (0, 1),
                                    (-1, -1),
                                    header_pad["bottom"],
                                ),
                                ("TOPPADDING", (0, 1), (-1, -1), header_pad["top"]),
                                ("LEFTPADDING", (0, 1), (-1, -1), header_pad["left"]),
                                ("RIGHTPADDING", (0, 1), (-1, -1), header_pad["right"]),
                                # Borders
                                (
                                    "GRID",
                                    (0, 0),
                                    (-1, -1),
                                    TABLE_CONFIG["border_width"],
                                    COLORS["border"],
                                ),
                                # Alternating row backgrounds
                                (
                                    "ROWBACKGROUNDS",
                                    (0, 1),
                                    (-1, -1),
                                    [COLORS["row_light"], COLORS["row_dark"]],
                                ),
                            ]
                        )
                    )

                else:
                    # Key-value style for simple lists
                    list_data = []
                    section_header = section_name.replace("_", " ").title()

                    for i, item in enumerate(section_data, 1):
                        # Create Paragraph objects for text wrapping
                        key_para = Paragraph(f"{section_header} {i}", header_cell_style)
                        value_para = Paragraph(str(item), value_cell_style)
                        list_data.append([key_para, value_para])

                    # Use consistent header width calculated earlier
                    table = Table(list_data, colWidths=[header_width, value_width])

                    # Modern styling for list table (same as dictionary tables)
                    header_pad = TABLE_CONFIG["padding"]["header"]
                    value_pad = TABLE_CONFIG["padding"]["value"]

                    table.setStyle(
                        TableStyle(
                            [
                                # First column (keys) styling as headers
                                ("BACKGROUND", (0, 0), (0, -1), COLORS["header_bg"]),
                                ("TEXTCOLOR", (0, 0), (0, -1), COLORS["header_text"]),
                                (
                                    "FONTNAME",
                                    (0, 0),
                                    (0, -1),
                                    TABLE_CONFIG["header_font"],
                                ),
                                (
                                    "FONTSIZE",
                                    (0, 0),
                                    (0, -1),
                                    TABLE_CONFIG["header_font_size"],
                                ),
                                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                                ("VALIGN", (0, 0), (0, -1), "TOP"),
                                (
                                    "BOTTOMPADDING",
                                    (0, 0),
                                    (0, -1),
                                    header_pad["bottom"],
                                ),
                                ("TOPPADDING", (0, 0), (0, -1), header_pad["top"]),
                                ("LEFTPADDING", (0, 0), (0, -1), header_pad["left"]),
                                ("RIGHTPADDING", (0, 0), (0, -1), header_pad["right"]),
                                # Second column (values) styling
                                ("TEXTCOLOR", (1, 0), (1, -1), colors.black),
                                (
                                    "FONTNAME",
                                    (1, 0),
                                    (1, -1),
                                    TABLE_CONFIG["value_font"],
                                ),
                                (
                                    "FONTSIZE",
                                    (1, 0),
                                    (1, -1),
                                    TABLE_CONFIG["value_font_size"],
                                ),
                                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                                ("VALIGN", (1, 0), (1, -1), "TOP"),
                                ("BOTTOMPADDING", (1, 0), (1, -1), value_pad["bottom"]),
                                ("TOPPADDING", (1, 0), (1, -1), value_pad["top"]),
                                ("LEFTPADDING", (1, 0), (1, -1), value_pad["left"]),
                                ("RIGHTPADDING", (1, 0), (1, -1), value_pad["right"]),
                                # Borders - default width
                                (
                                    "GRID",
                                    (0, 0),
                                    (-1, -1),
                                    TABLE_CONFIG["border_width"],
                                    COLORS["border"],
                                ),
                                (
                                    "LINEBELOW",
                                    (0, 0),
                                    (0, -1),
                                    TABLE_CONFIG["border_width"],
                                    COLORS["border"],
                                ),
                                # Alternating row backgrounds for the value column
                                (
                                    "ROWBACKGROUNDS",
                                    (1, 0),
                                    (1, -1),
                                    [COLORS["row_light"], COLORS["row_dark"]],
                                ),
                            ]
                        )
                    )

                story.append(table)
                story.append(Spacer(1, 8))  # Reduced from 15
        else:
            # Handle simple string/number values with enhanced styling
            story.append(
                Paragraph(section_name.replace("_", " ").title(), heading_style)
            )

            # Create a styled box for simple values
            value_text = str(section_data)
            if len(value_text) > 100:  # Long text gets normal styling
                story.append(Paragraph(value_text, normal_style))
            else:  # Short text gets highlighted box
                value_box = Table([[value_text]], colWidths=[DOC_CONFIG["total_width"]])
                value_box.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), COLORS["light_bg"]),
                            ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["text"]),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 12),
                            ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                            ("TOPPADDING", (0, 0), (-1, 0), 10),
                            ("LEFTPADDING", (0, 0), (-1, 0), 15),
                            ("RIGHTPADDING", (0, 0), (-1, 0), 15),
                            ("GRID", (0, 0), (-1, 0), 1, COLORS["primary"]),
                        ]
                    )
                )
                story.append(value_box)
            story.append(Spacer(1, 8))  # Reduced from 15

    # Add footer with generation timestamp
    story.append(Spacer(1, 30))
    footer_divider = Table(
        [[""]], colWidths=[DOC_CONFIG["total_width"]], rowHeights=[1]
    )
    footer_divider.setStyle(
        TableStyle(
            [
                ("LINEABOVE", (0, 0), (-1, 0), 1, COLORS["border"]),
            ]
        )
    )
    story.append(footer_divider)

    timestamp = datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p")
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=9,
        textColor=HexColor("#6C757D"),
        fontName="Helvetica",
        alignment=TA_CENTER,
        spaceAfter=0,
    )
    story.append(Paragraph(timestamp, footer_style))

    # Build PDF
    logger.info("Building PDF document with ReportLab...")
    doc.build(story)
    logger.info(f"PDF report generated successfully: {filename}")
    return filename


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


if __name__ == "__main__":
    main()
