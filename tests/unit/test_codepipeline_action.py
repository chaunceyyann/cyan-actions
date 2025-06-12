import pytest
import yaml
import os

def test_codepipeline_action_exists():
    """Test that the codepipeline-planonly action exists."""
    action_path = ".github/actions/codepipeline-planonly/action.yml"
    assert os.path.exists(action_path), f"Action file {action_path} should exist"

def test_codepipeline_action_structure():
    """Test that the codepipeline-planonly action has the expected structure."""
    action_path = ".github/actions/codepipeline-planonly/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    # Test basic structure
    assert 'name' in action, "Action should have a name"
    assert 'description' in action, "Action should have a description"
    assert 'inputs' in action, "Action should have inputs"
    assert 'runs' in action, "Action should have runs configuration"

def test_codepipeline_action_inputs():
    """Test that the codepipeline-planonly action has expected inputs."""
    action_path = ".github/actions/codepipeline-planonly/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    inputs = action.get('inputs', {})
    
    # Test required AWS inputs
    required_inputs = [
        'aws-target-account',
        'aws-pipeline-account', 
        'aws-region',
        'commit-sha',
        'aws-access-key-id',
        'aws-secret-access-key'
    ]
    
    for input_name in required_inputs:
        assert input_name in inputs, f"Should have {input_name} input"
        assert inputs[input_name]['required'] == True, f"{input_name} should be required"

def test_codepipeline_action_is_composite():
    """Test that the codepipeline-planonly action is a composite action."""
    action_path = ".github/actions/codepipeline-planonly/action.yml"
    
    with open(action_path, 'r') as f:
        action = yaml.safe_load(f)
    
    runs = action.get('runs', {})
    assert runs.get('using') == 'composite', "Should be a composite action"
    assert 'steps' in runs, "Composite action should have steps" 