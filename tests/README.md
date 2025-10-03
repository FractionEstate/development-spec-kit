# Specify CLI Tests

Automated test suite for the Specify CLI using pytest.

## Running Tests

### Install test dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install pytest pytest-cov
```

### Run all tests

```bash
pytest tests/
```

### Run with coverage

```bash
pytest tests/ --cov=src/specify_cli --cov-report=html --cov-report=term
```

### Run specific test file

```bash
pytest tests/test_init.py -v
```

### Run specific test

```bash
pytest tests/test_init.py::test_init_with_model_flag -v
```

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_init.py` - Tests for `specify init` command
- `test_status.py` - Tests for `specify status` command
- `test_models.py` - Tests for model catalog and validation
- `test_validation.py` - Tests for CLI validation and error handling

## Test Coverage

The test suite covers:

### Functional Tests

- ✅ Interactive init with model selection
- ✅ Non-interactive init (piped input)
- ✅ Model preselection with `--model` flag
- ✅ Invalid model validation and suggestions
- ✅ Status command (default, JSON, agent modes)
- ✅ List models command
- ✅ Version and help commands
- ✅ Check prerequisites command

### Edge Cases

- ✅ Empty model name (defaults to gpt-4o)
- ✅ Non-TTY environments (no hang)
- ✅ Invalid model names (helpful suggestions)
- ✅ Network failures (fallback catalog)
- ✅ Missing required files
- ✅ Workspace detection errors

### Integration Tests

- ✅ GitHub Models API integration
- ✅ Claude model variants (8 models)
- ✅ Cache mechanism (1-hour TTL)
- ✅ File creation (prompts, instructions, context)
- ✅ VS Code settings generation

## CI/CD Integration

Tests run automatically in GitHub Actions:

- `.github/workflows/test.yml` - Main test workflow
- `.github/workflows/lint.yml` - Linting (ruff, pyright, markdownlint)
- `.github/workflows/security.yml` - Security scanning (bandit, pip-audit)
- `.github/workflows/build.yml` - Package building and validation

## Expected Results

All tests should pass:

```text
===================== test session starts ======================
platform linux -- Python 3.12.x, pytest-8.x.x, pluggy-1.x.x
rootdir: /workspaces/development-spec-kit
plugins: cov-5.x.x
collected 20 items

tests/test_init.py ....            [ 20%]
tests/test_status.py ....          [ 40%]
tests/test_models.py .....         [ 65%]
tests/test_validation.py .......   [100%]

===================== 20 passed in 5.23s =======================
```

## Adding New Tests

When adding features, ensure tests cover:

1. **Happy path** - Feature works as expected
2. **Error cases** - Invalid inputs handled gracefully
3. **Edge cases** - Boundary conditions, empty values, etc.
4. **Integration** - Works with other CLI commands

Example test template:

```python
def test_new_feature(temp_workspace):
    """Test description."""
    result = subprocess.run(
        ["specify", "command", "args"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "expected output" in result.stdout
```
