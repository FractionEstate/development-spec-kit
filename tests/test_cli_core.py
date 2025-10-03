"""
Core CLI functionality tests - focused on actual CLI behavior.
"""

import subprocess
import json
from pathlib import Path


def test_version_command():
    """Test specify version command."""
    result = subprocess.run(
        ["specify", "version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_help_command():
    """Test specify --help command."""
    result = subprocess.run(
        ["specify", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "init" in result.stdout
    assert "status" in result.stdout
    assert "list-models" in result.stdout


def test_list_models_command():
    """Test specify list-models command."""
    result = subprocess.run(
        ["specify", "list-models"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    # Should list major models
    assert "gpt-4o" in result.stdout
    assert "claude" in result.stdout.lower()


def test_list_models_includes_claude():
    """Test that list-models includes Claude models."""
    result = subprocess.run(
        ["specify", "list-models"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    # Check for any Claude mention
    assert "claude-sonnet" in result.stdout.lower() or "claude sonnet" in result.stdout.lower()


def test_check_command():
    """Test specify check command."""
    result = subprocess.run(
        ["specify", "check"],
        capture_output=True,
        text=True,
    )

    # Should succeed
    assert result.returncode == 0
    assert "git" in result.stdout.lower() or "visual studio code" in result.stdout.lower()


def test_invalid_command():
    """Test invalid command shows help."""
    result = subprocess.run(
        ["specify", "invalid-command"],
        capture_output=True,
        text=True,
    )

    # Should fail
    assert result.returncode != 0
