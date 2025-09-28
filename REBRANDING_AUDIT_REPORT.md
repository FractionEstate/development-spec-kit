# Rebranding Audit Report
**Project**: Development Spec Kit
**New Repository**: `FractionEstate/development-spec-kit`
**Previous Repository**: `github/spec-kit`
**Audit Date**: September 27, 2025

## Executive Summary

This audit identifies all hardcoded references to the previous repository (`github/spec-kit`) that need to be updated to reflect the new organization and repository name (`FractionEstate/development-spec-kit`). The audit covers documentation, source code, configuration files, templates, and scripts.

## Critical Issues Found

### 🔴 **HIGH PRIORITY** - Source Code Repository References

**Location**: `src/specify_cli/__init__.py`
**Lines**: 437-438, 444
**Current**:
```python
repo_owner = "github"
repo_name = "spec-kit"
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
```
**Required Action**: Update to `FractionEstate` and `development-spec-kit`

### 🔴 **HIGH PRIORITY** - Badge URLs in README

**Location**: `README.md` line 11
**Current**:
```markdown
[![Release](https://github.com/github/spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/github/spec-kit/actions/workflows/release.yml)
```
**Required Action**: Update to `FractionEstate/development-spec-kit`

### 🔴 **HIGH PRIORITY** - Installation Commands

**Multiple Locations** - All installation commands reference the old repository:
- `README.md` lines 49, 64
- `docs/installation.md` lines 18, 24, 26, 34-36, 50-51, 59
- `docs/quickstart.md` lines 14, 19-20
- `docs/local-development.md` lines 10, 63

**Example**:
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

## Medium Priority Issues

### 🟡 **MEDIUM PRIORITY** - Documentation Configuration

**Location**: `docs/docfx.json` line 65
**Current**:
```json
"repo": "https://github.com/github/spec-kit"
```
**Required Action**: Update to `FractionEstate/development-spec-kit`

### 🟡 **MEDIUM PRIORITY** - Support Links

**Location**: `SUPPORT.md` line 9, `README.md` line 609
**Current**:
```markdown
- Open a [GitHub issue](https://github.com/github/spec-kit/issues/new)
```
**Required Action**: Update to `FractionEstate/development-spec-kit`

### 🟡 **MEDIUM PRIORITY** - Template References

**Location**: `templates/.github/copilot-references.md` line 137
**Current**:
```markdown
- **[Spec-Kit Repository](https://github.com/FractionEstate/spec-kit)** - This project's source
```
**Issue**: This already shows `FractionEstate/spec-kit` but should be `FractionEstate/development-spec-kit`

## Low Priority Issues

### 🟢 **LOW PRIORITY** - Historical References in CHANGELOG

**Location**: `CHANGELOG.md` - Multiple historical pull request references
**Lines**: 46, 47, 59, 65, 72, 84, 85
**Examples**:
- `[#394](https://github.com/github/spec-kit/pull/394)`
- `[#137](https://github.com/github/spec-kit/pull/137)`

**Recommendation**: Keep these as historical references since they point to actual past pull requests.

### 🟢 **LOW PRIORITY** - Code Comments

**Location**: `src/specify_cli/__init__.py` line 377
**Current**: `# See: https://github.com/github/spec-kit/issues/123`
**Recommendation**: Keep as historical reference to original issue.

## Files Requiring Updates

### Critical Files (Must Update)
1. **`src/specify_cli/__init__.py`** - Repository owner/name constants
2. **`README.md`** - Badge URLs and installation commands
3. **`docs/installation.md`** - All installation examples
4. **`docs/quickstart.md`** - Installation commands
5. **`docs/local-development.md`** - Development examples
6. **`docs/docfx.json`** - Documentation repository configuration
7. **`SUPPORT.md`** - Support link URLs
8. **`templates/.github/copilot-references.md`** - Repository reference

### Files That Are Correct
- **`pyproject.toml`** - No repository references (✓)
- **GitHub Workflows** - Use relative paths and environment variables (✓)
- **Scripts** - No hardcoded repository references (✓)

## Repository Name Decision

**Current Repository**: `FractionEstate/development-spec-kit`
**Previous Repository**: `github/spec-kit`

**Options**:
1. **Keep `development-spec-kit`** - Maintains current repository structure
2. **Rename to `spec-kit`** - Matches the original project name

**Recommendation**: Decide on final repository name first, then apply all updates consistently.

## Implementation Plan

### Phase 1: Core Functionality (Critical)
1. Update `src/specify_cli/__init__.py` repository constants
2. Update all installation commands in documentation
3. Update README.md badge URLs
4. Update support links

### Phase 2: Documentation (Medium Priority)
1. Update docfx.json repository configuration
2. Update template references
3. Test all documentation builds

### Phase 3: Validation
1. Test installation commands work with new repository
2. Verify badge URLs display correctly
3. Confirm support links navigate properly
4. Update version in `pyproject.toml` and `CHANGELOG.md`

## Search and Replace Patterns

### For Documentation Files
**Find**: `git+https://github.com/github/spec-kit.git`
**Replace**: `git+https://github.com/FractionEstate/development-spec-kit.git`

**Find**: `https://github.com/github/spec-kit`
**Replace**: `https://github.com/FractionEstate/development-spec-kit`

### For Source Code
**Find**: `repo_owner = "github"`
**Replace**: `repo_owner = "FractionEstate"`

**Find**: `repo_name = "spec-kit"`
**Replace**: `repo_name = "development-spec-kit"`

## Validation Checklist

After implementing changes:
- [ ] Installation commands work from new repository
- [ ] GitHub badges display correctly
- [ ] Support links navigate to correct repository
- [ ] Documentation builds successfully
- [ ] CLI tool downloads templates from correct repository
- [ ] All internal references are consistent

## Notes

1. **Version Bump Required**: Since `__init__.py` changes affect functionality, increment version in `pyproject.toml` and add entry to `CHANGELOG.md`

2. **Release Process**: Current GitHub workflows appear to be properly configured with relative paths and should work with the new repository name.

3. **Template Files**: Templates appear to have some references that are already using `FractionEstate` but with wrong repository name.

4. **Historical Links**: CHANGELOG entries referencing old pull requests should remain unchanged as they are historical records.
