#!/usr/bin/env python3
"""
Test runner for account-mapping action.
Run unit tests, integration tests, or both.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(test_type, verbose=False):
    """Run tests of the specified type."""
    script_dir = Path(__file__).parent
    tests_dir = script_dir / "tests"

    if test_type == "unit":
        test_path = tests_dir / "unit"
        print("Running unit tests...")
    elif test_type == "integration":
        test_path = tests_dir / "integration"
        print("Running integration tests...")
    elif test_type == "all":
        test_path = tests_dir
        print("Running all tests...")
    else:
        print(f"Unknown test type: {test_type}")
        return False

    if not test_path.exists():
        print(f"Test directory not found: {test_path}")
        return False

    # Build pytest command
    cmd = ["python", "-m", "pytest", str(test_path)]
    if verbose:
        cmd.append("-v")

    # Run tests
    try:
        subprocess.run(cmd, cwd=script_dir, check=True)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for account-mapping action")
    parser.add_argument(
        "test_type", choices=["unit", "integration", "all"], help="Type of tests to run"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    success = run_tests(args.test_type, args.verbose)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
