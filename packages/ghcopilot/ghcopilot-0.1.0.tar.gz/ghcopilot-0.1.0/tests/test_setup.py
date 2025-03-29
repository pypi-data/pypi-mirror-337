import os
import pytest
from unittest.mock import MagicMock
import importlib.util

@pytest.fixture
def setup_path():
    # Get the absolute path to the setup.py file
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'setup.py'))

@pytest.fixture
def setup_kwargs(setup_path, monkeypatch):
    # Load the setup.py as a module
    setup_spec = importlib.util.spec_from_file_location("setup_module", setup_path)
    module = importlib.util.module_from_spec(setup_spec)
    
    # Mock setuptools.setup
    mock_setup = MagicMock()
    monkeypatch.setattr('setuptools.setup', mock_setup)
    
    # Execute the setup.py file with our mock
    setup_spec.loader.exec_module(module)
    
    # Check that setup was called once
    assert mock_setup.call_count == 1
    
    # Return the kwargs passed to setup()
    _, kwargs = mock_setup.call_args
    return kwargs

def test_setup_file_exists(setup_path):
    """Test that setup.py file exists"""
    assert os.path.isfile(setup_path), "setup.py file does not exist"

def test_package_metadata(setup_kwargs):
    """Test package metadata in setup.py"""
    assert setup_kwargs['name'] == "copilotapi", "Package name should be 'copilotapi'"
    assert setup_kwargs['version'] == "0.1.0", "Package version should be '0.1.0'"
    assert setup_kwargs['description'] == "GitHub Copilot API + CLI", "Description does not match"
    assert setup_kwargs['author'] == "CodeSoft", "Author does not match"
    assert setup_kwargs['long_description_content_type'] == "text/markdown", "Content type should be markdown"

def test_dependencies(setup_kwargs):
    """Test dependencies in setup.py"""
    required_dependencies = ["requests", "selenium", "rich", "inquirer"]
    for dep in required_dependencies:
        assert dep in setup_kwargs['install_requires'], f"Dependency '{dep}' not found"

def test_entry_points(setup_kwargs):
    """Test entry points in setup.py"""
    assert 'console_scripts' in setup_kwargs['entry_points'], "Console scripts entry point not found"
    assert 'copilot=copilotapi.cli:main' in setup_kwargs['entry_points']['console_scripts'], \
           "CLI entry point not correctly configured"

def test_classifiers(setup_kwargs):
    """Test classifiers in setup.py"""
    required_classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
    for classifier in required_classifiers:
        assert classifier in setup_kwargs['classifiers'], f"Classifier '{classifier}' not found"

def test_python_version(setup_kwargs):
    """Test Python version requirement in setup.py"""
    assert setup_kwargs['python_requires'] == ">=3.6", "Python version requirement does not match"
