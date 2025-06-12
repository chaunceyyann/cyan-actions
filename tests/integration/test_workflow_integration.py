import pytest
import subprocess
import os
import yaml

@pytest.mark.integration
def test_changed_files_action_integration():
    """Integration test for changed-files action (requires git repository)."""
    # This would be a more complex test that actually runs the action
    # For now, just check that we're in a git repository
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    assert result.returncode == 0, "Should be in a git repository for integration tests"

@pytest.mark.integration  
def test_workflow_syntax_validation():
    """Test that all workflow files have valid YAML syntax."""
    workflows_dir = ".github/workflows"
    if os.path.exists(workflows_dir):
        for filename in os.listdir(workflows_dir):
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                filepath = os.path.join(workflows_dir, filename)
                with open(filepath, 'r') as f:
                    try:
                        yaml.safe_load(f)
                    except yaml.YAMLError as e:
                        pytest.fail(f"Invalid YAML in {filepath}: {e}") 