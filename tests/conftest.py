"""
Pytest configuration and fixtures for Specify CLI tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="specify-test-")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_github_token():
    """Provide a mock GitHub token for testing."""
    return "ghp_mock_token_for_testing_only"


@pytest.fixture
def sample_models():
    """Provide sample model data for testing."""
    return {
        "gpt-4o": "GPT-4o",
        "gpt-4o-mini": "GPT-4o mini",
        "claude-sonnet-4.5": "Claude Sonnet 4.5",
        "claude-sonnet-4": "Claude Sonnet 4",
        "llama-3.3-70b-instruct": "Llama 3.3 70B Instruct",
        "phi-4": "Phi-4",
    }
