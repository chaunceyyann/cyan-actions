import pytest
import yaml
import os

def test_changed_files_action_exists():
    """Test that the changed-files action exists."""
    action_path = ".github/actions/changed-files/action.yml"
    assert os.path.exists(action_path), f"Action file {action_path} should exist"

def test_changed_files_action_structure():
    """Test that the changed-files action has the expected structure."""
    action_path = ".github/actions/changed-files/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    # Test basic structure
    assert 'name' in action, "Action should have a name"
    assert 'description' in action, "Action should have a description"
    assert 'inputs' in action, "Action should have inputs"
    assert 'outputs' in action, "Action should have outputs"
    assert 'runs' in action, "Action should have runs configuration"

def test_changed_files_action_inputs():
    """Test that the changed-files action has expected inputs."""
    action_path = ".github/actions/changed-files/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    inputs = action.get('inputs', {})
    
    # Test pattern input
    assert 'pattern' in inputs, "Should have pattern input"
    assert inputs['pattern']['required'] == True, "Pattern input should be required"

def test_changed_files_action_outputs():
    """Test that the changed-files action has expected outputs."""
    action_path = ".github/actions/changed-files/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    outputs = action.get('outputs', {})
    
    # Test files output
    assert 'files' in outputs, "Should have files output"
    assert 'description' in outputs['files'], "files output should have description"

def test_changed_files_action_is_composite():
    """Test that the changed-files action is a composite action."""
    action_path = ".github/actions/changed-files/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    runs = action.get('runs', {})
    assert runs.get('using') == 'composite', "Should be a composite action"
    assert 'steps' in runs, "Composite action should have steps" 