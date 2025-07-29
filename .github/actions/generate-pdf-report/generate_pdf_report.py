#!/usr/bin/env python3
"""
PDF Report Generator for GitHub Actions.
Generates professional PDF reports using reportlab.
"""

import json
import logging
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


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


def debug_environment_variables():
    """Debug all environment variables used by the script."""
    logger = logging.getLogger(__name__)

    env_vars = [
        "REPORT_TITLE",
        "GENERATED_TIME",
        "REPOSITORY",
        "PR_NUMBER",
        "PR_TITLE",
        "EXECUTION_DETAILS",
        "COMMIT_INFORMATION",
        "QUALITY_CHECK",
        "PIPELINE_STATUS",
        "VARIABLES",
        "OUTPUT_FILENAME",
    ]

    logger.info("Debugging environment variables:")
    for var in env_vars:
        value = os.environ.get(var, "")
        if value:
            logger.debug(f"{var}: {value}")
        else:
            logger.warning(f"{var}: (empty or not set)")


def create_pdf_report():
    """Create a PDF report with the provided data."""
    logger = logging.getLogger(__name__)
    logger.info("Starting PDF report generation")

    # Debug environment variables
    debug_environment_variables()

    # Get inputs from environment variables
    report_title = os.environ.get("REPORT_TITLE", "Execution Report")
    generated_time = os.environ.get("GENERATED_TIME", "")
    repository = os.environ.get("REPOSITORY", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    pr_title = os.environ.get("PR_TITLE", "")

    # Parse JSON inputs with error handling
    try:
        execution_details = json.loads(os.environ.get("EXECUTION_DETAILS", "{}"))
        logger.debug(f"Parsed execution_details: {execution_details}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse EXECUTION_DETAILS: {e}")
        execution_details = {}

    try:
        commit_information = json.loads(os.environ.get("COMMIT_INFORMATION", "{}"))
        logger.debug(f"Parsed commit_information: {commit_information}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse COMMIT_INFORMATION: {e}")
        commit_information = {}

    try:
        quality_check = json.loads(os.environ.get("QUALITY_CHECK", "{}"))
        logger.debug(f"Parsed quality_check: {quality_check}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse QUALITY_CHECK: {e}")
        quality_check = {}

    try:
        pipeline_status = json.loads(os.environ.get("PIPELINE_STATUS", "{}"))
        logger.debug(f"Parsed pipeline_status: {pipeline_status}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse PIPELINE_STATUS: {e}")
        pipeline_status = {}

    variables = os.environ.get("VARIABLES", "")
    output_filename = os.environ.get("OUTPUT_FILENAME", "report")

    logger.info(f"Output filename: {output_filename}")

    # Create PDF document
    filename = f"{output_filename}.pdf"
    logger.info(f"Creating PDF document: {filename}")

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue,
    )
    normal_style = styles["Normal"]

    # Build story
    story = []

    # Title
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 20))

    # Metadata
    metadata_data = []
    if generated_time:
        formatted_time = format_timestamp(generated_time)
        metadata_data.append(["Generated", formatted_time])
    if repository:
        metadata_data.append(["Repository", repository])
    if pr_number and pr_title:
        metadata_data.append(["PR", f"#{pr_number} - {pr_title}"])
    elif pr_number:
        metadata_data.append(["PR", f"#{pr_number}"])

    if metadata_data:
        metadata_table = Table(metadata_data, colWidths=[2 * inch, 4 * inch])
        metadata_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
                ]
            )
        )
        story.append(metadata_table)
        story.append(Spacer(1, 20))

    # Pipeline Information (Execution Details + Pipeline Status)
    pipeline_info = {}
    if execution_details:
        pipeline_info.update(execution_details)
    if pipeline_status:
        pipeline_info.update(pipeline_status)

    if pipeline_info:
        story.append(Paragraph("Pipeline Information", heading_style))

        # Format timestamps in pipeline information
        formatted_pipeline_info = {}
        for k, v in pipeline_info.items():
            if k.lower() in ["start time", "starttime"]:
                formatted_pipeline_info[k] = format_timestamp(v)
            else:
                formatted_pipeline_info[k] = v

        pipeline_data = [[k, v] for k, v in formatted_pipeline_info.items()]
        pipeline_table = Table(pipeline_data, colWidths=[2 * inch, 4 * inch])
        pipeline_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
                ]
            )
        )
        story.append(pipeline_table)
        story.append(Spacer(1, 20))

    # Commit Information
    if commit_information:
        story.append(Paragraph("Commit Information", heading_style))

        # Format timestamp in commit information
        formatted_commit_info = {}
        for k, v in commit_information.items():
            if k.lower() == "timestamp":
                formatted_commit_info[k] = format_timestamp(v)
            else:
                formatted_commit_info[k] = v

        commit_data = [[k, v] for k, v in formatted_commit_info.items()]
        commit_table = Table(commit_data, colWidths=[2 * inch, 4 * inch])
        commit_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
                ]
            )
        )
        story.append(commit_table)
        story.append(Spacer(1, 20))

    # Quality Check
    if quality_check:
        story.append(Paragraph("Quality Check", heading_style))
        quality_data = [[k, v] for k, v in quality_check.items()]
        quality_table = Table(quality_data, colWidths=[2 * inch, 4 * inch])
        quality_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
                ]
            )
        )
        story.append(quality_table)
        story.append(Spacer(1, 20))

    # Add variables if available
    if variables and variables.strip():
        story.append(Spacer(1, 20))
        story.append(Paragraph("Variables", heading_style))
        story.append(Paragraph(f"<pre>{variables}</pre>", normal_style))

    # Build PDF
    logger.info("Building PDF document...")
    doc.build(story)
    logger.info(f"PDF report generated successfully: {filename}")
    return filename


def main():
    """Main function to generate PDF report."""
    logger = setup_logging()

    try:
        logger.info("Starting PDF generation process")
        filename = create_pdf_report()
        logger.info(f"Successfully generated PDF: {filename}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
