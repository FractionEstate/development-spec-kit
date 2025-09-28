# GitHub Models Integration Guide

## Overview

The FractionEstate Development Spec Kit is now dedicated to a single, opinionated workflow: **GitHub Models inside VS Code with GitHub Copilot Chat**. The Specify CLI bootstraps projects, installs the required GitHub Models prompts, and keeps configuration aligned with the Spec-Driven Development process. This document captures how the toolkit uses GitHub Models today and the maintenance touch points for future improvements.

## Supported Experience

When you run `specify init`, the CLI:

- Fetches the latest GitHub Models catalog (with caching to `~/.specify/models_cache.json`).
- Falls back to a curated list in `src/specify_cli/__init__.py` when the API is unavailable.
- Installs the `.github/prompts/` command set plus GitHub Copilot guidance files under `.github/`.
- Configures VS Code settings and tasks for Copilot-first development.
- Surfaces the selected model inside generated prompts so the agent stays anchored on your choice.

Only GitHub Models are supported. Legacy scripts and docs for other assistants (Claude, Gemini, Cursor, etc.) were archived with the multi-agent release packages for historical reference.

## Model Selection Flow

1. **Token handling** – The CLI checks the `--github-token` flag, then `GH_TOKEN`/`GITHUB_TOKEN` environment variables, and finally proceeds unauthenticated if no token is supplied.
2. **Catalog lookup** – `fetch_github_models()` retrieves models from `https://models.inference.ai.azure.com/models`, storing the normalized mapping `{model_id: display_name}`.
3. **Fallback safety net** – If the network call fails or returns no entries, the CLI calls `get_fallback_github_models()` for the curated map.
4. **Interactive selection** – `select_with_arrows()` renders the available models so you can choose the default for the generated project.
5. **Template injection** – The chosen model ID is written to GitHub Copilot prompt files (e.g., `.github/copilot-instructions.md`) and surfaced by status commands.

The same catalog powers:

- `specify init --model <model_id>` – Skip the interactive picker.
- `specify status` – Show the configured model for the current workspace.
- `specify list-models` – Display cached or live GitHub Models data.

## Customizing the Catalog

The curated fallback list lives in `get_fallback_github_models()` inside `src/specify_cli/__init__.py`. When GitHub announces new generally available models:

1. Add or update the mapping entry `{ "model-id": "Friendly Display Name" }`.
2. Bump the CLI version in `pyproject.toml`.
3. Record the change in `CHANGELOG.md` (under an "Added" or "Changed" section).
4. Run `uv build` or the release workflow to distribute the update.

If you need to patch the local cache quickly during development, delete `~/.specify/models_cache.json` or run `specify list-models --refresh` (the flag automatically clears stale caches).

## CLI Flags Related to GitHub Models

| Flag | Purpose |
|------|---------|
| `--model` | Preselect the GitHub Model during `specify init`. |
| `--github-token` | Provide a short-lived or PAT token to access private/preview models. |
| `--ignore-agent-tools` | Skip checks for VS Code/GitHub Copilot (useful in CI). |
| `specify list-models --refresh` | Force a new fetch and replace the local cache. |

## File Touch Points

| File | Purpose |
|------|---------|
| `src/specify_cli/__init__.py` | CLI commands, model discovery, fallback list, cache logic. |
| `.github/copilot-instructions.md` | Main Copilot chat guidance populated during init. |
| `.github/copilot-context.md` | Supplemental context for GitHub Models chats. |
| `.github/prompts/*.md` | Slash-command style prompts tailored for GitHub Models. |

When adjusting any of these files via the CLI, remember to keep the Spec Driven Development templates consistent (plan/spec/tasks) so Copilot conversations align with the curated workflow.

## Historical Context

Earlier releases of Spec Kit shipped multi-agent artifacts (Claude, Gemini, Cursor, Windsurf, etc.). Those packages remain in the `.genreleases/` directory tree for archival purposes but are **no longer maintained**. New work should focus exclusively on GitHub Models. If an enterprise deployment requires additional agents in the future, plan to:

1. Fork from the archived multi-agent release branch.
2. Reintroduce the relevant scripts/templates under a separate package.
3. Provide upgrade notes clarifying the divergence from the GitHub Models-first experience.

By keeping this document aligned with the GitHub Models roadmap, we ensure the CLI stays lightweight, focused, and ready for new model launches without reviving legacy code paths.
