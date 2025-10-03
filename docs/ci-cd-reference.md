# CI/CD Quick Reference

Quick guide to the GitHub Actions workflows for Specify CLI.

## Workflows Overview

| Workflow | Trigger | Purpose | Duration |
|----------|---------|---------|----------|
| **Lint** | Push, PR | Code quality checks | ~2 min |
| **Test** | Push, PR | Automated testing | ~5 min |
| **Build** | Push, PR, Release | Package building | ~3 min |
| **Security** | Push, PR, Weekly | Security scanning | ~4 min |

## Workflow Details

### 1. Lint Workflow

**File**: `.github/workflows/lint.yml`

#### Jobs

- **markdown-lint**: Validates all Markdown files
- **python-lint**: Runs ruff and pyright

#### Commands to run locally

```bash
# Markdown linting
markdownlint-cli2 **/*.md

# Python linting
ruff check src/

# Type checking
pyright src/
```

### 2. Test Workflow

**File**: `.github/workflows/test.yml`

#### Jobs

- **cli-validation**: Tests CLI commands on Python 3.11, 3.12, 3.13
- **edge-case-testing**: Tests error handling and edge cases

#### Commands to run locally

```bash
# Run pytest
pytest tests/ -v

# Run specific test
pytest tests/test_cli_core.py::test_version_command -v

# Test with coverage
pytest tests/ --cov=src/specify_cli --cov-report=term
```

### 3. Build Workflow

**File**: `.github/workflows/build.yml`

#### Jobs

- **build-package**: Builds wheel and source distribution
- **publish-to-pypi**: Auto-publishes on release (trusted publishing)

#### Commands to run locally

```bash
# Build package
uv build

# Check package contents
tar -tzf dist/*.tar.gz | head -20

# Test installation
uv tool install dist/*.whl
specify version
```

### 4. Security Workflow

**File**: `.github/workflows/security.yml`

#### Jobs

- **security-scan**: Runs Bandit, pip-audit, Safety
- **dependency-review**: Reviews dependencies in PRs

#### Commands to run locally

```bash
# Install security tools
uv pip install bandit safety pip-audit

# Run Bandit
bandit -r src/

# Run pip-audit
pip-audit --desc

# Check for vulnerabilities
safety check
```

## Deployment Validation

**Script**: `scripts/validate-deployment.sh`

Runs comprehensive validation before deployment.

```bash
# Run validation
bash scripts/validate-deployment.sh

# Expected output: All 23 checks passing
```

### Validation Checks

1. **Code Quality** (2)
   - Markdown linting
   - Python files present

2. **CLI Functionality** (4)
   - version, help, list-models, check commands

3. **Model Catalog** (4)
   - 50+ models, Claude, GPT-4o, Claude Sonnet 4.5

4. **Documentation** (5)
   - README, CHANGELOG, AGENTS.md, docs/, tests/

5. **Package Building** (3)
   - Build succeeds, wheel created, source dist

6. **CI/CD** (4)
   - All workflow files present

7. **Tests** (1)
   - Pytest runs successfully

## Common Tasks

### Before Committing

```bash
# 1. Run linting
markdownlint-cli2 **/*.md
ruff check src/

# 2. Run tests
pytest tests/ -v

# 3. Build package
uv build

# 4. Run deployment validation
bash scripts/validate-deployment.sh
```

### Creating a Release

```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG.md
# 3. Commit changes
git add .
git commit -m "chore: Prepare release v1.0.3"

# 4. Create and push tag
git tag v1.0.3
git push origin main --tags

# 5. Monitor GitHub Actions
# Build workflow will auto-publish to PyPI
```

### Debugging Failed Workflows

#### Lint Failures

```bash
# Fix markdown
markdownlint-cli2 --fix **/*.md

# Fix Python
ruff check --fix src/
```

#### Test Failures

```bash
# Run failed test with verbose output
pytest tests/test_cli_core.py::test_name -vv

# Debug with print statements (captured with -s)
pytest tests/ -s
```

#### Build Failures

```bash
# Clean and rebuild
rm -rf dist/ build/
uv build

# Validate package
twine check dist/*
```

## Monitoring

### GitHub Actions Tab

- View workflow runs: `https://github.com/{org}/{repo}/actions`
- Check workflow logs for detailed output
- Review failed steps and error messages

### Status Badges

Add to README.md:

```markdown
[![Lint](https://github.com/{org}/{repo}/workflows/Lint/badge.svg)](https://github.com/{org}/{repo}/actions/workflows/lint.yml)
[![Test](https://github.com/{org}/{repo}/workflows/Test/badge.svg)](https://github.com/{org}/{repo}/actions/workflows/test.yml)
[![Build](https://github.com/{org}/{repo}/workflows/Build/badge.svg)](https://github.com/{org}/{repo}/actions/workflows/build.yml)
```

## Secrets Configuration

Required secrets for full automation:

| Secret | Purpose | Required For |
|--------|---------|--------------|
| `GITHUB_TOKEN` | Auto-generated | All workflows |
| `PYPI_API_TOKEN` | PyPI publishing | Build workflow (if not using trusted publishing) |

### Trusted Publishing (Recommended)

Configure at: `https://pypi.org/manage/account/publishing/`

- No secrets needed
- More secure
- Automatic on release

## Troubleshooting

### Common Issues

1. **Workflow not triggering**
   - Check trigger conditions in workflow file
   - Ensure branch name matches
   - Verify push/PR includes changed files

2. **Tests failing in CI but passing locally**
   - Check Python version matrix
   - Verify dependencies are installed
   - Review environment differences

3. **Build failing**
   - Ensure `pyproject.toml` is valid
   - Check all dependencies are listed
   - Verify package structure

4. **Security scan failures**
   - Review Bandit report
   - Update vulnerable dependencies
   - Add security exceptions if needed

## Quick Commands Reference

```bash
# Lint
markdownlint-cli2 **/*.md
ruff check src/

# Test
pytest tests/ -v

# Build
uv build

# Validate
bash scripts/validate-deployment.sh

# Install
uv tool install dist/*.whl

# Release
git tag v1.0.3 && git push --tags
```

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [uv Documentation](https://docs.astral.sh/uv/)

---

Last Updated: 2024-10-03
