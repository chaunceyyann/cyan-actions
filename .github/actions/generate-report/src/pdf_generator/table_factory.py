#!/usr/bin/env python3
"""
Table Factory and Table Classes for PDF generation.
"""

import json
from abc import ABC, abstractmethod

from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle

from .config import COLORS, DOC_CONFIG, TABLE_CONFIG
from .utils import (
    capitalize_header_text,
    create_header_cell_style,
    create_value_cell_style,
    format_value,
)


class BaseTable(ABC):
    """Abstract base class for all table types."""

    def __init__(self, styles):
        self.styles = styles
        self.header_cell_style = create_header_cell_style(styles["base_styles"])
        self.value_cell_style = create_value_cell_style(styles["base_styles"])

    @abstractmethod
    def create(self, data):
        """Create and return a table."""
        pass

    def _calculate_column_widths(self, data):
        """Calculate column widths based on content."""
        if isinstance(data, dict):
            max_key_length = max(len(capitalize_header_text(k)) for k in data.keys())
            header_width = max(
                DOC_CONFIG["min_header_width"],
                max_key_length * DOC_CONFIG["header_char_width"]
                + DOC_CONFIG["header_padding"],
            )
            value_width = DOC_CONFIG["total_width"] - header_width
            return header_width, value_width
        return None, None


class DictTable(BaseTable):
    """Table for dictionary data (key-value pairs)."""

    def create(self, data):
        """Create a simple key-value table from dictionary."""
        if not data:
            return None

        # Build table data
        table_data = []
        for key, value in data.items():
            header_text = capitalize_header_text(key)
            formatted_value = format_value(value)

            key_para = Paragraph(header_text, self.header_cell_style)
            value_para = Paragraph(str(formatted_value), self.value_cell_style)
            table_data.append([key_para, value_para])

        if not table_data:
            return None

        # Calculate widths
        header_width, value_width = self._calculate_column_widths(data)

        # Create table
        table = Table(table_data, colWidths=[header_width, value_width])
        table.setStyle(self._get_style())

        return table

    def _get_style(self):
        """Get styling for dictionary tables."""
        header_pad = TABLE_CONFIG["padding"]["header"]
        value_pad = TABLE_CONFIG["padding"]["value"]

        return TableStyle(
            [
                # Header column styling
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
                # Value column styling
                ("TEXTCOLOR", (1, 0), (1, -1), colors.black),
                ("FONTNAME", (1, 0), (1, -1), TABLE_CONFIG["value_font"]),
                ("FONTSIZE", (1, 0), (1, -1), TABLE_CONFIG["value_font_size"]),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (1, 0), (1, -1), "TOP"),
                ("BOTTOMPADDING", (1, 0), (1, -1), value_pad["bottom"]),
                ("TOPPADDING", (1, 0), (1, -1), value_pad["top"]),
                ("LEFTPADDING", (1, 0), (1, -1), value_pad["left"]),
                ("RIGHTPADDING", (1, 0), (1, -1), value_pad["right"]),
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
                    (1, 0),
                    (1, -1),
                    [COLORS["row_light"], COLORS["row_dark"]],
                ),
            ]
        )


class MergedTable(BaseTable):
    """Table with merged cells for lists of values (like found_lines)."""

    def create(self, data):
        """Create table with merged cells for lists of values."""
        if not data:
            return None

        # Build table data with merge tracking
        table_data = []
        merge_ranges = {}
        current_row = 0

        for key, values in data.items():
            key_text = capitalize_header_text(key)
            key_para = Paragraph(key_text, self.header_cell_style)

            # Handle found_lines data specifically
            if key == "found_lines":
                if isinstance(values, str):
                    try:
                        # Parse JSON string back to dictionary
                        parsed_values = json.loads(values)
                        if isinstance(parsed_values, dict):
                            # Flatten the dictionary into a list of key-value pairs
                            value_list = []
                            for pattern, lines in parsed_values.items():
                                if isinstance(lines, list):
                                    for line in lines:
                                        value_list.append(f"{pattern}: {line.strip()}")
                                else:
                                    value_list.append(f"{pattern}: {lines.strip()}")
                        else:
                            value_list = [values]  # Fallback to original string
                    except (json.JSONDecodeError, TypeError):
                        value_list = [values]  # Fallback to original string
                elif isinstance(values, dict):
                    # Handle dictionary directly (when not formatted as JSON string)
                    value_list = []
                    for pattern, lines in values.items():
                        if isinstance(lines, list):
                            for line in lines:
                                value_list.append(f"{pattern}: {line.strip()}")
                        else:
                            value_list.append(f"{pattern}: {lines.strip()}")
                else:
                    value_list = [values]  # Fallback
            else:
                # Handle both single values and lists
                if isinstance(values, list):
                    value_list = values
                else:
                    value_list = [values]

            if value_list:
                # Track merge range
                start_row = current_row
                end_row = current_row + len(value_list) - 1
                merge_ranges[key] = (start_row, end_row)

                # Add each value as separate row
                for value in value_list:
                    value_para = Paragraph(str(value), self.value_cell_style)
                    table_data.append([key_para, value_para])
                    current_row += 1

        if not table_data:
            return None

        # Calculate widths
        header_width, value_width = self._calculate_column_widths(data)

        # Create table
        table = Table(table_data, colWidths=[header_width, value_width])
        table.setStyle(self._get_style(merge_ranges))

        return table

    def _get_style(self, merge_ranges):
        """Get styling for merged tables."""
        header_pad = TABLE_CONFIG["padding"]["header"]
        value_pad = TABLE_CONFIG["padding"]["value"]

        style_commands = [
            # Header column styling
            ("BACKGROUND", (0, 0), (0, -1), COLORS["header_bg"]),
            ("TEXTCOLOR", (0, 0), (0, -1), COLORS["header_text"]),
            ("FONTNAME", (0, 0), (0, -1), TABLE_CONFIG["header_font"]),
            ("FONTSIZE", (0, 0), (0, -1), TABLE_CONFIG["header_font_size"]),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (0, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (0, -1), header_pad["bottom"]),
            ("TOPPADDING", (0, 0), (0, -1), header_pad["top"]),
            ("LEFTPADDING", (0, 0), (0, -1), header_pad["left"]),
            ("RIGHTPADDING", (0, 0), (0, -1), header_pad["right"]),
            # Value column styling
            ("TEXTCOLOR", (1, 0), (1, -1), colors.black),
            ("FONTNAME", (1, 0), (1, -1), TABLE_CONFIG["value_font"]),
            ("FONTSIZE", (1, 0), (1, -1), TABLE_CONFIG["value_font_size"]),
            ("ALIGN", (1, 0), (1, -1), "LEFT"),
            ("VALIGN", (1, 0), (1, -1), "TOP"),
            ("BOTTOMPADDING", (1, 0), (1, -1), value_pad["bottom"]),
            ("TOPPADDING", (1, 0), (1, -1), value_pad["top"]),
            ("LEFTPADDING", (1, 0), (1, -1), value_pad["left"]),
            ("RIGHTPADDING", (1, 0), (1, -1), value_pad["right"]),
            # Borders
            ("GRID", (0, 0), (-1, -1), TABLE_CONFIG["border_width"], COLORS["border"]),
            # Alternating row backgrounds
            (
                "ROWBACKGROUNDS",
                (1, 0),
                (1, -1),
                [COLORS["row_light"], COLORS["row_dark"]],
            ),
        ]

        # Add merge commands
        for key, (start_row, end_row) in merge_ranges.items():
            if start_row != end_row:
                style_commands.append(("SPAN", (0, start_row), (0, end_row)))

        return TableStyle(style_commands)


class TraditionalTable(BaseTable):
    """Traditional table with headers at top."""

    def create(self, data):
        """Create traditional table with headers at top."""
        if not data or not isinstance(data, list) or len(data) == 0:
            return None

        # Get all keys from first item
        all_keys = list(data[0].keys())

        # Create header row
        header_row = [
            Paragraph(capitalize_header_text(key), self.header_cell_style)
            for key in all_keys
        ]
        table_data = [header_row]

        # Create data rows
        for item in data:
            row = [
                Paragraph(str(format_value(item.get(key, ""))), self.value_cell_style)
                for key in all_keys
            ]
            table_data.append(row)

        # Calculate column widths
        num_cols = len(all_keys)
        col_width = DOC_CONFIG["total_width"] / num_cols
        col_widths = [col_width] * num_cols

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(self._get_style())

        return table

    def _get_style(self):
        """Get styling for traditional tables."""
        header_pad = TABLE_CONFIG["padding"]["value"]

        return TableStyle(
            [
                # Header row styling
                ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
                ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["header_text"]),
                ("FONTNAME", (0, 0), (-1, 0), TABLE_CONFIG["header_font"]),
                ("FONTSIZE", (0, 0), (-1, 0), TABLE_CONFIG["header_font_size"]),
                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                ("VALIGN", (0, 0), (-1, 0), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 12),
                # Data rows styling
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("FONTNAME", (0, 1), (-1, -1), TABLE_CONFIG["value_font"]),
                ("FONTSIZE", (0, 1), (-1, -1), TABLE_CONFIG["value_font_size"]),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 1), (-1, -1), header_pad["bottom"]),
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


class ListTable(BaseTable):
    """Table for simple lists."""

    def create(self, data, section_name):
        """Create simple list table."""
        if not data:
            return None

        list_data = []
        section_header = capitalize_header_text(section_name)

        for i, item in enumerate(data, 1):
            key_para = Paragraph(f"{section_header} {i}", self.header_cell_style)
            value_para = Paragraph(str(item), self.value_cell_style)
            list_data.append([key_para, value_para])

        if not list_data:
            return None

        # Calculate widths
        header_width = 1.5 * 72  # 1.5 inches
        value_width = DOC_CONFIG["total_width"] - header_width

        table = Table(list_data, colWidths=[header_width, value_width])
        table.setStyle(self._get_style())

        return table

    def _get_style(self):
        """Get styling for list tables."""
        header_pad = TABLE_CONFIG["padding"]["header"]
        value_pad = TABLE_CONFIG["padding"]["value"]

        return TableStyle(
            [
                # First column styling as headers
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
                # Second column styling
                ("TEXTCOLOR", (1, 0), (1, -1), COLORS["text"]),
                ("FONTNAME", (1, 0), (1, -1), TABLE_CONFIG["value_font"]),
                ("FONTSIZE", (1, 0), (1, -1), TABLE_CONFIG["value_font_size"]),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (1, 0), (1, -1), "TOP"),
                ("BOTTOMPADDING", (1, 0), (1, -1), value_pad["bottom"]),
                ("TOPPADDING", (1, 0), (1, -1), value_pad["top"]),
                ("LEFTPADDING", (1, 0), (1, -1), value_pad["left"]),
                ("RIGHTPADDING", (1, 0), (1, -1), value_pad["right"]),
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
                    (1, 0),
                    (1, -1),
                    [COLORS["row_light"], COLORS["row_dark"]],
                ),
            ]
        )


class ValueBox:
    """Simple value box for short text."""

    def __init__(self, styles):
        self.styles = styles

    def create(self, value_text):
        """Create a simple value box."""
        table = Table([[value_text]], colWidths=[DOC_CONFIG["total_width"]])
        table.setStyle(
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
        return table


class Divider:
    """Divider elements."""

    def __init__(self, styles):
        self.styles = styles

    def create_title_divider(self):
        """Create a title divider."""
        divider = Table([[""]], colWidths=[DOC_CONFIG["total_width"]], rowHeights=[1])
        divider.setStyle(
            TableStyle(
                [
                    ("LINEABOVE", (0, 0), (-1, 0), 1, COLORS["primary"]),
                    ("BACKGROUND", (0, 0), (-1, 0), COLORS["light_bg"]),
                ]
            )
        )
        return divider

    def create_footer_divider(self):
        """Create a footer divider."""
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
        return footer_divider


class TableFactory:
    """Factory class for creating different types of tables."""

    def __init__(self, styles):
        self.styles = styles
        self.dict_table = DictTable(styles)
        self.merged_table = MergedTable(styles)
        self.traditional_table = TraditionalTable(styles)
        self.list_table = ListTable(styles)
        self.value_box = ValueBox(styles)
        self.divider = Divider(styles)

    def create_dict_table(self, data):
        """Create a dictionary table."""
        return self.dict_table.create(data)

    def create_merged_table(self, data):
        """Create a merged table."""
        return self.merged_table.create(data)

    def create_traditional_table(self, data):
        """Create a traditional table."""
        return self.traditional_table.create(data)

    def create_list_table(self, data, section_name):
        """Create a list table."""
        return self.list_table.create(data, section_name)

    def create_value_box(self, value_text):
        """Create a value box."""
        return self.value_box.create(value_text)

    def create_title_divider(self):
        """Create a title divider."""
        return self.divider.create_title_divider()

    def create_footer_divider(self):
        """Create a footer divider."""
        return self.divider.create_footer_divider()
