#!/usr/bin/env python3
"""
Simple local test for PDF and HTML report generation.
Assumes dependencies are already installed.
"""

import json
import os
from datetime import datetime

# Import our report generation modules
from generate_json_pdf import create_pdf_report
from generate_markdown_html import create_html_report


def create_test_data():
    """Create simple test data."""
    return {
        "title": "Test Report - Table Styles Comparison",
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
        "notes": "This is a test report generated locally.",
    }


def test_pdf():
    """Test PDF generation with key-value style."""
    print("Testing PDF generation (key-value style)...")

    test_data = create_test_data()
    os.environ["REPORT_DATA"] = json.dumps(test_data)
    os.environ["OUTPUT_FILENAME"] = "test_report_keyvalue"

    try:
        filename = create_pdf_report()
        if os.path.exists(filename):
            print(f"✅ PDF created: {filename}")
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
        filename = create_html_report()
        if os.path.exists(filename):
            print(f"✅ HTML created: {filename}")
            return True
        else:
            print("❌ HTML file not created")
            return False
    except Exception as e:
        print(f"❌ HTML error: {e}")
        return False


def test_traditional_table_style():
    """Test traditional table style (headers at top)."""
    print("Testing traditional table style (headers at top)...")

    # This would require modifying the PDF generator to support a flag
    # For now, we'll just show what the current style looks like
    print("📝 Note: Current implementation uses key-value style for all data.")
    print("   To see traditional table style, you would need to modify the generator.")
    print("   Current style shows headers in first column, values in second column.")
    return True


def main():
    """Run tests."""
    print("🚀 Testing report generation...")
    print("=" * 50)

    # Test current key-value style
    pdf_success = test_pdf()
    html_success = test_html()

    # Show table style info
    table_info = test_traditional_table_style()

    print("\n📊 Results:")
    print(f"  PDF (key-value): {'✅' if pdf_success else '❌'}")
    print(f"  HTML: {'✅' if html_success else '❌'}")
    print(f"  Table style info: {'✅' if table_info else '❌'}")

    if pdf_success or html_success:
        print("\n🎉 Test completed!")
        print("\n📋 Table Style Comparison:")
        print(
            "  • Key-Value Style (current): Headers in first column, values in second"
        )
        print("  • Traditional Table Style: Headers at top row, data below")
        print("  • See test_report_keyvalue.pdf for current style example")
    else:
        print("\n⚠️  No tests passed.")


if __name__ == "__main__":
    main()
