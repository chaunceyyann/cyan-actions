#!/usr/bin/env python3
"""
PDF Report Generator for GitHub Actions.
Generates professional PDF reports using reportlab.
"""

import json
import logging
import os
import sys

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


def debug_environment_variables():
    """Debug all environment variables used by the script."""
    logger = logging.getLogger(__name__)

    env_vars = [
        "REPORT_TITLE",
        "GENERATED_TIME",
        "WORKFLOW_NAME",
        "RUN_ID",
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
    workflow_name = os.environ.get("WORKFLOW_NAME", "")
    run_id = os.environ.get("RUN_ID", "")
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
        metadata_data.append(["Generated", generated_time])
    if workflow_name:
        metadata_data.append(["Workflow", workflow_name])
    if run_id:
        metadata_data.append(["Run ID", run_id])
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

    # Execution Details
    if execution_details:
        story.append(Paragraph("Execution Details", heading_style))
        exec_data = [[k, v] for k, v in execution_details.items()]
        exec_table = Table(exec_data, colWidths=[2 * inch, 4 * inch])
        exec_table.setStyle(
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
        story.append(exec_table)
        story.append(Spacer(1, 20))

    # Commit Information
    if commit_information:
        story.append(Paragraph("Commit Information", heading_style))
        commit_data = [[k, v] for k, v in commit_information.items()]
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

    # Pipeline Status
    if pipeline_status:
        story.append(Paragraph("Pipeline Status", heading_style))
        status_data = [[k, v] for k, v in pipeline_status.items()]
        status_table = Table(status_data, colWidths=[2 * inch, 4 * inch])
        status_table.setStyle(
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
        story.append(status_table)

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
