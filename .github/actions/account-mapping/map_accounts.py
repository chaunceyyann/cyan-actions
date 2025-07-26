#!/usr/bin/env python3
"""
Account mapping script for GitHub Actions.
Reads account mappings from mappings.yml and determines account based on changed files.
"""

import os
import sys
from pathlib import Path

import yaml


def load_mappings():
    """Load account mappings from mappings.yml file."""
    script_dir = Path(__file__).parent
    mappings_file = script_dir / "mappings.yml"

    # Debug: Print current working directory and file paths
    print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
    print(f"Script directory: {script_dir}", file=sys.stderr)
    print(f"Mappings file path: {mappings_file}", file=sys.stderr)
    print(f"Mappings file exists: {mappings_file.exists()}", file=sys.stderr)

    try:
        with open(mappings_file, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: mappings.yml not found at {mappings_file}", file=sys.stderr)
        print("Available files in script directory:", file=sys.stderr)
        for file in script_dir.iterdir():
            print(f"  - {file.name}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in mappings.yml: {e}", file=sys.stderr)
        sys.exit(1)


def extract_directories(changed_files):
    """Extract first directory from each file path."""
    if not changed_files:
        return set()

    directories = set()
    for file_path in changed_files.strip().split():
        if file_path:
            parts = file_path.split("/")
            if len(parts) > 1:
                directories.add(parts[0])

    return directories


def determine_account_types(directories):
    """Determine account types based on directories found."""
    account_types = []

    # Map directories to account types
    directory_mapping = {
        "src": "src",
        "tests": "tests",
        # Add more mappings here as needed
    }

    for directory in directories:
        if directory in directory_mapping:
            account_types.append(directory_mapping[directory])

    return account_types


def main():
    """Main function to determine account number."""
    # Get inputs from environment variables
    changed_files = os.environ.get("CHANGED_FILES", "")
    environment = os.environ.get("ENVIRONMENT", "")

    # Load account mappings
    account_mappings = load_mappings()

    # Extract directories from changed files
    directories = extract_directories(changed_files)

    # Determine account types
    account_types = determine_account_types(directories)

    if not account_types:
        print(
            f"No matching directory found in changed files. "
            f"Found directories: {directories}",
            file=sys.stderr,
        )
        print("Skipping workflow - no account mapping available", file=sys.stderr)
        # Return a special value to indicate no mapping found
        print("account_number=SKIP")
        print("mapping_found=false")
        return

    # Get account numbers from mapping
    if environment not in account_mappings:
        print(f"Error: Unknown environment '{environment}'", file=sys.stderr)
        sys.exit(1)

    account_numbers = []
    for account_type in account_types:
        if account_type not in account_mappings[environment]:
            print(
                f"Error: Unknown account type '{account_type}' "
                f"for environment '{environment}'",
                file=sys.stderr,
            )
            sys.exit(1)
        account_numbers.append(account_mappings[environment][account_type])

    # Join multiple account numbers with comma (or choose one based on priority)
    account_number = ",".join(account_numbers)

    # Output for GitHub Actions
    print(f"account_number={account_number}")
    print("mapping_found=true")
    print(f"Environment: {environment}", file=sys.stderr)
    print(f"Changed files: {changed_files}", file=sys.stderr)
    print(f"Directories found: {directories}", file=sys.stderr)
    print(f"Account types: {account_types}", file=sys.stderr)
    print(f"Account numbers: {account_numbers}", file=sys.stderr)
    print(f"Final account number: {account_number}", file=sys.stderr)


if __name__ == "__main__":
    main()
