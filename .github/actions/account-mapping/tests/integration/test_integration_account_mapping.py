import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestAccountMappingIntegration(unittest.TestCase):
    """Integration tests for account mapping action."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.script_dir = Path(__file__).parent.parent
        self.original_cwd = os.getcwd()

        # Create a test mappings file
        self.mappings_file = self.script_dir / "mappings.yml"
        test_mappings = """
dev:
  src: "123456789012"
  tests: "987654321098"
prod:
  src: "111111111111"
  tests: "222222222222"
"""
        with open(self.mappings_file, "w") as f:
            f.write(test_mappings)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)

    def test_script_execution_with_valid_inputs(self):
        """Test that the script executes successfully with valid inputs."""
        # Set up environment variables
        env = os.environ.copy()
        env["CHANGED_FILES"] = "src/file1.py tests/test1.py"
        env["ENVIRONMENT"] = "dev"

        # Run the script
        result = subprocess.run(
            ["python3", str(self.script_dir / "map_accounts.py")],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.script_dir,
        )

        # Check that the script ran successfully
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

        # Check that the output contains the expected account number
        self.assertIn("account_number=123456789012,987654321098", result.stdout)

        # Check that debug information is printed to stderr
        self.assertIn("Environment: dev", result.stderr)
        self.assertIn("Changed files: src/file1.py tests/test1.py", result.stderr)

    def test_script_execution_with_single_file_type(self):
        """Test that the script works with only one file type."""
        env = os.environ.copy()
        env["CHANGED_FILES"] = "src/file1.py src/file2.py"
        env["ENVIRONMENT"] = "dev"

        result = subprocess.run(
            ["python3", str(self.script_dir / "map_accounts.py")],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.script_dir,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("account_number=123456789012", result.stdout)

    def test_script_execution_with_no_matching_files(self):
        """Test that the script fails when no matching files are found."""
        env = os.environ.copy()
        env["CHANGED_FILES"] = "docs/readme.md config/settings.yml"
        env["ENVIRONMENT"] = "dev"

        result = subprocess.run(
            ["python3", str(self.script_dir / "map_accounts.py")],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.script_dir,
        )

        # Script should exit with error code 1
        self.assertEqual(result.returncode, 1)
        self.assertIn("No matching directory found", result.stderr)

    def test_script_execution_with_unknown_environment(self):
        """Test that the script fails with unknown environment."""
        env = os.environ.copy()
        env["CHANGED_FILES"] = "src/file1.py"
        env["ENVIRONMENT"] = "unknown"

        result = subprocess.run(
            ["python3", str(self.script_dir / "map_accounts.py")],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.script_dir,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Unknown environment 'unknown'", result.stderr)

    def test_script_execution_with_empty_changed_files(self):
        """Test that the script fails with empty changed files."""
        env = os.environ.copy()
        env["CHANGED_FILES"] = ""
        env["ENVIRONMENT"] = "dev"

        result = subprocess.run(
            ["python3", str(self.script_dir / "map_accounts.py")],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.script_dir,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("No matching directory found", result.stderr)

    def test_script_execution_with_prod_environment(self):
        """Test that the script works with prod environment."""
        env = os.environ.copy()
        env["CHANGED_FILES"] = "src/file1.py tests/test1.py"
        env["ENVIRONMENT"] = "prod"

        result = subprocess.run(
            ["python3", str(self.script_dir / "map_accounts.py")],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.script_dir,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("account_number=111111111111,222222222222", result.stdout)
        self.assertIn("Environment: prod", result.stderr)


if __name__ == "__main__":
    unittest.main()
