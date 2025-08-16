#!/usr/bin/env python3
"""
Simple local test for PDF and HTML report generation.
Assumes dependencies are already installed.
"""

import json
import os

# Add the src directory to the path
import sys
from datetime import datetime

src_path = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, src_path)

from html_generator.run import HTMLGenerator

# Import our report generation modules
from pdf_generator.run import PDFGenerator


def create_comprehensive_test_data():
    """Create comprehensive test data with all possible table scenarios."""
    return {
        "title": "Comprehensive Test Report - All Table Scenarios",
        "basic_info": {
            "project": (
                "Test Project very loooooooooooooooooooooooong name that should test "
                "how the PDF generator handles extremely long text in table cells "
                "and whether it wraps properly or gets cut off"
            ),
            "version": "1.0.0",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active",
        },
        "jira_ticket": "JIRA-1234: Test Feature Implementation",
        "repository": "test-org/test-repo",
        "pr_information": {
            "number": "42",
            "title": "JIRA-1234: Test Feature Implementation",
            "author": "test-user",
        },
        "commit_information": {
            "sha": "abc123def456",
            "message": "feat: implement test feature",
            "author": "Test User",
            "timestamp": "2024-01-15T10:30:00Z",
            "branch": "feature/test-feature",
            "base_ref": "main",
        },
        "quality_check": {
            "patterns_checked": "TODO,FIXME,HACK,BUG",
            "sensitive_keywords_found": "true",
            "found_lines": {
                "TODO": [
                    "// TODO: Implement user authentication system",
                    "// TODO: Add error handling for edge cases",
                    "  TODO: Fix the bug in the login function",
                    "// TODO: Update documentation",
                ],
                "FIXME": [
                    "// FIXME: This is a temporary workaround for the performance issue",
                    "// FIXME: Need to investigate the memory leak",
                    "  FIXME: Security vulnerability needs to be addressed",
                ],
                "HACK": [
                    "// HACK: Bypassing validation for now",
                    "// HACK: Quick fix for the deadline",
                    "  HACK: Temporary solution until proper implementation",
                ],
                "BUG": ["// BUG: There's a critical bug in the payment system"],
            },
        },
        "pipeline_status": {
            "execution_id": "test-execution-123",
            "status": "Succeeded",
            "start_time": "2024-01-15T10:30:00Z",
            "platform": "AWS",
            "target_account": "123456789012",
            "aws_region": "us-east-1",
            "variables": "Environment: staging, Version: 1.0.0",
            "console_url": "https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/test-pipeline/executions/test-execution-123/view?region=us-east-1",
        },
        "activities": [
            "Code review completed",
            "Tests passed",
            "Deployment successful",
        ],
        "team_members": [
            {"name": "John Doe", "role": "Developer", "email": "john.doe@example.com"},
            {
                "name": "Jane Smith",
                "role": "QA Engineer",
                "email": "jane.smith@example.com",
            },
            {"name": "Bob Wilson", "role": "DevOps", "email": "bob.wilson@example.com"},
            {
                "name": "Alice Johnson",
                "role": (
                    "Senior Software Engineer with very loooooooooooooooooooooooong "
                    "title that should test text wrapping"
                ),
                "email": "alice.johnson@example.com",
            },
        ],
        "test_scenarios": {
            "empty_dict": {},
            "empty_list": [],
            "null_value": None,
            "boolean_values": {"true_value": True, "false_value": False},
            "numeric_values": {
                "integer": 42,
                "float": 3.14159,
                "zero": 0,
                "negative": -1,
            },
            "special_characters": {
                "quotes": "Text with 'single' and \"double\" quotes",
                "newlines": "Line 1\nLine 2\nLine 3",
                "tabs": "Column1\tColumn2\tColumn3",
                "unicode": "Café, naïve, résumé, 你好, こんにちは",
            },
        },
        "pr_url": "https://github.com/test-org/test-repo/pull/42",
        "notes": "This is a comprehensive test report with all possible table scenarios including URLs, long text, special characters, and various data types.",
    }


def test_comprehensive_pdf():
    """Test PDF generation with comprehensive data covering all scenarios."""
    print("Testing comprehensive PDF generation (all table scenarios)...")

    test_data = create_comprehensive_test_data()
    os.environ["REPORT_DATA"] = json.dumps(test_data)
    os.environ["OUTPUT_FILENAME"] = "test_comprehensive_report"

    try:
        generator = PDFGenerator(test_data, "test_comprehensive_report")
        filename = generator.generate()
        if os.path.exists(filename):
            print(f"✅ Comprehensive PDF created: {filename}")
            return True
        else:
            print("❌ PDF file not created")
            return False
    except Exception as e:
        print(f"❌ PDF error: {e}")
        return False


def test_html():
    """Test HTML generation."""
    print("Testing HTML generation...")

    # Use README.md as test markdown content
    readme_path = "../../../README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        print(f"✅ Loaded README from: {readme_path}")
    except FileNotFoundError:
        print(f"⚠️  README not found at {readme_path}, using fallback content")
        markdown_content = (
            """# Test Report

## Project Information
- **Project**: Test Project
- **Version**: 1.0.0
- **Status**: Active
- **Created**: """
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + """

## Activities
- Code review completed
- Tests passed
- Deployment successful

## Notes
This is a test report generated locally using Markdown and Grip.
"""
        )

    os.environ["REPORT_DATA"] = markdown_content
    os.environ["OUTPUT_FILENAME"] = "test_report"

    try:
        generator = HTMLGenerator(markdown_content, "test_report")
        filename = generator.generate()
        if os.path.exists(filename):
            print(f"✅ HTML created: {filename}")
            return True
        else:
            print("❌ HTML file not created")
            return False
    except Exception as e:
        print(f"❌ HTML error: {e}")
        return False


def main():
    """Run tests."""
    print("🚀 Testing comprehensive report generation...")
    print("=" * 50)

    # Test comprehensive PDF generation
    pdf_success = test_comprehensive_pdf()
    html_success = test_html()

    print("\n📊 Results:")
    print(f"  Comprehensive PDF: {'✅' if pdf_success else '❌'}")
    print(f"  HTML: {'✅' if html_success else '❌'}")

    if pdf_success or html_success:
        print("\n🎉 Test completed!")
        print("\n📋 Generated Files:")
        print("  • test_comprehensive_report.pdf - All table scenarios in one PDF")
        print("  • test_report.html - HTML report")
        print("\n📋 Comprehensive PDF Testing:")
        print("  • Basic info with long text wrapping")
        print("  • JIRA ticket and repository info")
        print("  • PR and commit information")
        print("  • Quality check with found_lines (TODO, FIXME, HACK, BUG)")
        print("  • Pipeline status with URLs")
        print("  • Team members with long role titles")
        print("  • Test scenarios with various data types:")
        print("    - Empty dictionaries and lists")
        print("    - Null values")
        print("    - Boolean values (true/false)")
        print("    - Numeric values (integers, floats, zero, negative)")
        print("    - Special characters (quotes, newlines, tabs, unicode)")
        print("  • URLs that should appear in blue")
    else:
        print("\n⚠️  No tests passed.")


if __name__ == "__main__":
    main()
