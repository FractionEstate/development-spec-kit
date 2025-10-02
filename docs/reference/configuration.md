# Configuration reference

Workspaces store state in a few predictable locations. Understanding these files makes it easier to troubleshoot, script upgrades, or integrate Spec Kit with existing tooling.

## Project-level configuration

### `.specify/config/models.json`

Persisted when you run `specify init`.

```json
{
  "github_models": {
    "selected_model": "gpt-4.1",
    "last_updated": "2025-10-02T15:12:48Z",
    "catalog_source": "api",
    "catalog_cached_at": "2025-10-02T15:11:01Z"
  },
  "scripts": {
    "preferred": "sh",
    "folder": "bash",
    "extension": "sh",
    "last_updated": "2025-10-02T15:12:48Z"
  }
}
```

- `selected_model` mirrors the GitHub Model chosen during initialization.
- `last_updated` records when the selection was made (UTC).
- `catalog_source` reflects the last catalog fetch (`api` or `fallback`).
- `catalog_cached_at` captures when the catalog cache was written.
- `scripts` describes which flavor (bash or PowerShell) the prompts target.

### `.github/prompts/*.prompt.md`

Generated from `.specify/templates/commands/`. Each file corresponds to a slash command and contains:

- Front-matter description.
- Inline instructions tailored for GitHub Copilot Chat.
- Placeholder replacements for `{SCRIPT}` and `$ARGUMENTS` performed by the CLI.

### `.github/copilot-instructions.md` & `.github/copilot-context.md`

Primary and supporting instructions consumed by GitHub Copilot Chat. Update them when you introduce new workflows or change the constitution.

### `.specify/templates/`

Project-specific copies of the templates. When the upstream kit releases new templates, running `specify init --here` merges updates without deleting local customisations.

## Global cache and metadata

### `~/.specify/models_cache.json`

Stores the GitHub Models catalog for reuse across projects.

- Refreshed automatically once per hour.
- Contains `models`, `timestamp`, and `source` keys.
- Clear with `specify list-models --clear-cache` or bypass with `--no-cache`.

### `~/.specify/models_cache.json.lock`

Created transiently during cache writes to prevent corruption. Automatically removed when the write succeeds.

## Keeping configuration fresh

1. **Update the catalog** – run `specify list-models --refresh` to fetch new GitHub Models.
2. **Switch models** – re-run `specify init --here --model <id>` or edit `.specify/config/models.json` and regenerate prompts via the CLI.
3. **Change script flavor** – rerun `specify init --here --script <sh or ps>` to regenerate prompts with the new script flavor.
4. **Reset documentation** – rerun `specify init --here` to merge the latest instructions, prompts, and templates into your workspace.
