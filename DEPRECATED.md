# Deprecated and Archived Content

This document explains what content in this repository is deprecated, archived, or maintained for compatibility.

## 📦 Archived content

### `.genreleases/` - Legacy multi-agent packages

**Status:** Archived (read-only)
**Reason:** Specify now exclusively targets GitHub Copilot with GitHub Models

The `.genreleases/` directory contains packaged releases from when Specify supported multiple AI assistants (Claude Desktop, Gemini, Cursor, Windsurf, etc.). These packages are **no longer maintained** but remain in the repository for:

- Historical reference
- Users on older versions who need access to previous releases
- Documentation of the evolution toward the current GitHub Models-only approach

**Action required:** None. These files are ignored by the main workflow and don't affect current functionality.

**Migration path:** If you're using an old multi-agent release, migrate to the current GitHub Copilot-based workflow by running:

```bash
specify init . --model claude-sonnet-4.5

```text

---

## 📝 Redirect files

### `docs/installation.md` and `docs/quickstart.md`

**Status:** Redirect stubs
**Reason:** Documentation was reorganized under `docs/getting-started/`

These files contain redirects to the new locations. They exist to prevent broken bookmarks and links.

**Actual locations:**

- `docs/getting-started/installation.md`
- `docs/getting-started/quickstart.md`

**Action required:** Update your bookmarks if you have them saved.

---

## 🔄 Migration-only files

### `README-OLD.md` (if present)

**Status:** Temporary backup
**Reason:** Created during README improvement to maintain old version temporarily

This file can be safely deleted after confirming the new README works correctly.

---

## 🚫 Never deprecated

The following are **actively maintained** and should never be treated as deprecated:

- `src/specify_cli/__init__.py` - Main CLI implementation
- `templates/` - Prompt and template files
- `scripts/` - Installation and workflow scripts
- `.github/workflows/` - CI/CD pipelines
- `docs/` (except redirect stubs) - Active documentation
- `memory/constitution.md` - Project principles
- `AGENTS.md` - GitHub Models integration guide

---

## 📋 Deprecation policy

When we deprecate features or files:

1. **Announce** in CHANGELOG.md with clear migration path
2. **Mark** files with deprecation notices
3. **Maintain** for at least one major version
4. **Archive** in appropriate directories with documentation
5. **Remove** only after transition period (minimum 6 months)

---

## ❓ Questions?

If you're unsure whether something is deprecated:

1. Check this file first
2. Review [CHANGELOG.md](CHANGELOG.md) for announcements
3. Run `specify --help` for current commands
4. Open a [Discussion](https://github.com/FractionEstate/development-spec-kit/discussions)

Last updated: October 3, 2025
