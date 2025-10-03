# CLI reference

The `specify` CLI bootstraps and maintains Spec Kit workspaces. Commands are implemented with [Typer](https://typer.tiangolo.com/) and packaged as a uv tool.

## `specify init`

Create a new workspace or refresh the current directory with the latest template.

```bash
specify init <project-name>
```

### Key options

| Flag | Description |
| ---- | ----------- |
| `--model <id>` | Preselect a GitHub Model (e.g. `gpt-4.1`, `gpt-4o-mini`). When omitted, an interactive picker appears. |
| `--script <sh or ps>` | Override script flavor (defaults to `sh` on POSIX, `ps` on Windows). |
| `--here` | Initialize the current directory instead of creating a new folder. |
| `--force` | Skip confirmation when using `--here` inside a non-empty directory. |
| `--github-token <token>` | Provide a token for private or preview models (falls back to `GH_TOKEN` / `GITHUB_TOKEN`). |
| `--no-git` | Skip `git init` even if Git is available. |
| `--ignore-agent-tools` | Bypass Copilot/VS Code environment checks. |

### What it does

1. Fetches the GitHub Models catalog (using cache when possible).
2. Lets you choose a model and script flavor.
3. Downloads the release archive and extracts it to the project directory.
4. Generates Copilot prompt files, wiring them to the chosen script flavor.
5. Persists configuration in `.specify/config/models.json`.
6. Prints next steps tailored for GitHub Copilot Chat.

## `specify check`

Validates local prerequisites (Git, VS Code/VS Code Insiders, and GitHub Models integration).

```bash
specify check
```

Use this command after installing the CLI or when setting up a new workstation.

## `specify list-models`

Displays the available GitHub Models.

```bash
specify list-models
specify list-models --refresh  # bypass cache
specify list-models --no-cache # fetch live catalog without writing cache
```

### Helpful flags for `status`

| Flag | Description |
| ---- | ----------- |
| `--github-token <token>` | Authenticate to see private/preview models. |
| `--verbose` | Show API endpoint and authentication hints. |
| `--no-cache` | Skip the local cache entirely. |
| `--clear-cache` | Remove the cached catalog and exit. |

The command reports cache age and source (API or fallback). Use `--refresh` to force a new fetch.

## `specify status`

Summarizes the current workspace.

```bash
specify status
```

Outputs include:

- Confirmation that `.specify/` exists.
- The number of available Copilot prompt commands.
- Selected GitHub Model, when it was set, and which catalog supplied it (API or fallback).
- Script flavor (bash or PowerShell) wired into the prompt templates.
- Age of the cached model catalog with a reminder command to refresh it.
- A "Workflow Artifacts" dashboard summarizing constitution/spec/plan/task coverage with suggested next slash commands.
- A feature progress table (first five features) with stage completion indicators and next recommended action.
- A highlighted "Next step" callout distilled from the dashboard follow-ups.
- Git repository status for the current directory.

### Helpful flags

| Flag | Description |
| ---- | ----------- |
| `--json` | Print the entire status payload as JSON (includes workflow summary, feature states, prompts, scripts, cache metadata, and next-step suggestions). |
| `--agent` | Emit a compact, plain-text summary tailored for automation agents (no banner, includes next step, feature matrix, and follow-up list). |

Use the JSON output when integrating with automation or when you need to inspect every feature beyond the first five shown in the table.

## `specify version`

Displays version metadata and cache information.

```bash
specify version
```

Shows the CLI version (or `development` if running from source), Python runtime, platform, and cache status (fresh/stale/none).

## Environment variables

| Variable | Description |
| -------- | ----------- |
| `GH_TOKEN` / `GITHUB_TOKEN` | Suppy a GitHub token for private model catalogs. CLI flags override environment variables. |
| `SPECIFY_DEBUG` | When set, surfaces additional diagnostics during extraction. |

## Cache files

`~/.specify/models_cache.json` stores the GitHub Models catalog with metadata:

```json
{
  "models": { "gpt-4.1": "GPT-4.1", "gpt-4o": "GPT-4o" },
  "timestamp": 1748451200.123,
  "source": "api"
}
```

- Cache is reused for 60 minutes by default.
- `specify list-models --refresh` rebuilds it immediately.
- Fallback catalogs are written with `"source": "fallback"` when the API is unreachable.
