import pytest
import yaml
import os

def test_python_ci_workflow_exists():
    """Test that the python-ci.yml workflow file exists."""
    workflow_path = ".github/workflows/python-ci.yml"
    assert os.path.exists(workflow_path), f"Workflow file {workflow_path} should exist"

def test_python_ci_workflow_structure():
    """Test that the python-ci.yml workflow has the expected structure."""
    workflow_path = ".github/workflows/python-ci.yml"
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Test basic structure
    assert 'name' in workflow, "Workflow should have a name"
    assert 'on' in workflow, "Workflow should have triggers"
    assert 'jobs' in workflow, "Workflow should have jobs"
    
    # Test workflow_call trigger
    assert 'workflow_call' in workflow['on'], "Should support workflow_call"
    
    # Test expected jobs
    expected_jobs = ['lint', 'unit-test', 'integration-test']
    for job in expected_jobs:
        assert job in workflow['jobs'], f"Should have {job} job"

def test_python_ci_inputs():
    """Test that the python-ci.yml workflow has expected inputs."""
    workflow_path = ".github/workflows/python-ci.yml"
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    inputs = workflow['on']['workflow_call'].get('inputs', {})
    
    # Test python-version input
    assert 'python-version' in inputs, "Should have python-version input"
    assert inputs['python-version']['default'] == '3.11', "Default Python version should be 3.11"
    
    # Test run-integration-tests input
    assert 'run-integration-tests' in inputs, "Should have run-integration-tests input"
    assert inputs['run-integration-tests']['type'] == 'boolean', "run-integration-tests should be boolean"
    assert inputs['run-integration-tests']['default'] == True, "run-integration-tests should default to true"

def test_integration_test_conditional():
    """Test that integration-test job has proper conditional."""
    workflow_path = ".github/workflows/python-ci.yml"
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    integration_job = workflow['jobs']['integration-test']
    assert 'if' in integration_job, "integration-test job should have conditional"
    assert "inputs.run-integration-tests == 'true'" in integration_job['if'] or \
           "inputs.run-integration-tests == true" in integration_job['if'], \
           "integration-test should check run-integration-tests input" 