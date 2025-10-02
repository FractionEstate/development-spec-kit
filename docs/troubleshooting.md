# Troubleshooting

Use these recipes when the Spec Kit CLI or Copilot workflows misbehave.

## Catalog or model selection issues

### `specify list-models` fails

- Ensure you are running Python 3.11+ and have network access.
- Retry with `specify list-models --refresh` to bypass stale caches.
- For private/preview models, pass a token: `specify list-models --github-token <TOKEN>`.
- If the API remains unavailable, the CLI falls back to the curated GitHub Models list and records `"source": "fallback"` in the cache.

### Model cache looks stale

- `specify status` reports cache age; refresh with `specify list-models --refresh`.
- Remove the cache manually: `specify list-models --clear-cache`.
- Cached data lives at `~/.specify/models_cache.json`.

## Workspace setup warnings

### `specify status` shows "No GitHub Models prompts found"

- Run `specify init --here` from the workspace root to regenerate prompts.
- Ensure `.github/prompts/` exists and contains `.prompt.md` files.

### Wrong script flavor wired into prompts

- Re-run `specify init --here --script <sh or ps>` to rebuild prompts with the desired flavor.
- Confirm `.specify/config/models.json` → `scripts.preferred` matches your expectation.

### Copilot ignores instructions

- Check `.github/copilot-instructions.md` for recent updates.
- Use the Command Palette → “Copilot: Refresh prompts” (Insiders) or reload VS Code.
- Confirm the repo is open at the workspace root (Copilot respects `.github/` relative paths).

## Git or environment problems

### `specify check` reports missing VS Code

- Install [VS Code](https://code.visualstudio.com/) or VS Code Insiders and add it to your `PATH`.
- On macOS, ensure `code` is available via the “Shell Command: Install 'code' command in PATH” option.

### Git not detected

- Install Git and restart your shell.
- On Windows, ensure Git is included in the system `PATH`.

## Documentation build failures

- Install the DocFX tool: `dotnet tool install -g docfx`.
- From `docs/`, run `docfx docfx.json --serve` and inspect the console output.
- Fix broken links reported by the `link-check` GitHub Actions workflow before pushing.

## When all else fails

1. Run `specify version` and `specify status` and gather the output.
2. Open an issue with logs at [github.com/FractionEstate/development-spec-kit/issues](https://github.com/FractionEstate/development-spec-kit/issues/new/choose).
3. Include OS, Python version, and whether you are behind a proxy or VPN.
