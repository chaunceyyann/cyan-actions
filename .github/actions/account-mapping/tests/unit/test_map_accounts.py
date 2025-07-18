import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add the parent directory to the path so we can import map_accounts
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import after path modification
import map_accounts  # noqa: E402


class TestMapAccounts(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mappings_file = Path(self.temp_dir) / "mappings.yml"

        # Create a test mappings file
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
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("map_accounts.Path")
    def test_load_mappings(self, mock_path):
        """Test loading mappings from YAML file."""
        # Mock the script directory to point to our temp directory
        mock_path.return_value.parent = Path(self.temp_dir)

        mappings = map_accounts.load_mappings()

        self.assertIn("dev", mappings)
        self.assertIn("prod", mappings)
        self.assertEqual(mappings["dev"]["src"], "123456789012")
        self.assertEqual(mappings["dev"]["tests"], "987654321098")

    def test_extract_directories(self):
        """Test extracting directories from changed files."""
        changed_files = "src/file1.py tests/test1.py docs/readme.md"
        directories = map_accounts.extract_directories(changed_files)

        expected = {"src", "tests", "docs"}
        self.assertEqual(directories, expected)

    def test_extract_directories_empty(self):
        """Test extracting directories from empty string."""
        directories = map_accounts.extract_directories("")
        self.assertEqual(directories, set())

    def test_extract_directories_single_file(self):
        """Test extracting directories from single file."""
        directories = map_accounts.extract_directories("file.txt")
        self.assertEqual(directories, set())

    def test_determine_account_types(self):
        """Test determining account types from directories."""
        directories = {"src", "tests", "docs"}
        account_types = map_accounts.determine_account_types(directories)

        expected = ["src", "tests"]
        self.assertEqual(account_types, expected)

    def test_determine_account_types_no_match(self):
        """Test determining account types with no matching directories."""
        directories = {"docs", "config"}
        account_types = map_accounts.determine_account_types(directories)

        self.assertEqual(account_types, [])

    @patch("os.environ.get")
    @patch("map_accounts.load_mappings")
    def test_main_success(self, mock_load_mappings, mock_env_get):
        """Test successful main function execution."""
        # Mock environment variables
        mock_env_get.side_effect = lambda key, default="": {
            "CHANGED_FILES": "src/file1.py tests/test1.py",
            "ENVIRONMENT": "dev",
        }.get(key, default)

        # Mock mappings
        mock_load_mappings.return_value = {
            "dev": {"src": "123456789012", "tests": "987654321098"}
        }

        # Capture stdout
        from io import StringIO

        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            map_accounts.main()
            output = mock_stdout.getvalue()

            self.assertIn("account_number=123456789012,987654321098", output)

    @patch("os.environ.get")
    def test_main_no_changed_files(self, mock_env_get):
        """Test main function with no changed files."""
        mock_env_get.side_effect = lambda key, default="": {
            "CHANGED_FILES": "",
            "ENVIRONMENT": "dev",
        }.get(key, default)

        with self.assertRaises(SystemExit):
            map_accounts.main()

    @patch("os.environ.get")
    def test_main_unknown_environment(self, mock_env_get):
        """Test main function with unknown environment."""
        mock_env_get.side_effect = lambda key, default="": {
            "CHANGED_FILES": "src/file1.py",
            "ENVIRONMENT": "unknown",
        }.get(key, default)

        with self.assertRaises(SystemExit):
            map_accounts.main()


if __name__ == "__main__":
    unittest.main()
