# Local Development Guide

How to iterate on the `specify` CLI locally without publishing a release or committing to `main`.

> Scripts ship in both Bash (`.sh`) and PowerShell (`.ps1`) variants. The CLI auto-selects based on OS unless you pass `--script sh|ps`.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Git
- Optional: VS Code + GitHub Copilot with access to GitHub Models

## 1. Clone and Switch Branches

```bash
git clone https://github.com/FractionEstate/development-spec-kit.git
cd development-spec-kit
# Work on a feature branch
git checkout -b your-feature-branch
```

## 2. Run the CLI Directly (Fastest Feedback)

You can execute the CLI via the module entrypoint without installing anything:

```bash
# From repo root
python -m src.specify_cli --help
python -m src.specify_cli init demo-project --model gpt-4o --ignore-agent-tools --script sh
```

If you prefer invoking the script file style (uses shebang):

```bash
python src/specify_cli/__init__.py init demo-project --script ps
```

## 3. Editable install (isolated environment)

Create an isolated environment using `uv` so dependencies resolve exactly like end users get them:

```bash
# Create & activate virtual env (uv auto-manages .venv)
uv venv
source .venv/bin/activate  # or on Windows PowerShell: .venv\Scripts\Activate.ps1

# Install project in editable mode
uv pip install -e .

# Now 'specify' entrypoint is available
specify --help
```

Re-running after code edits requires no reinstall because of editable mode.

## 4. Invoke with uvx directly from Git (current branch)

`uvx` can run from a local path (or a Git ref) to simulate user flows:

```bash
uvx --from . specify init demo-uvx --model gpt-4o --ignore-agent-tools --script sh
```

You can also point uvx at a specific branch without merging:

```bash
# Push your working branch first
git push origin your-feature-branch
uvx --from git+https://github.com/FractionEstate/development-spec-kit.git@your-feature-branch specify init demo-branch-test --script ps
```

### 4a. Absolute path uvx (run from anywhere)

If you're in another directory, use an absolute path instead of `.`:

```bash
uvx --from /mnt/c/GitHub/development-spec-kit specify --help
uvx --from /mnt/c/GitHub/development-spec-kit specify init demo-anywhere --model gpt-4o --ignore-agent-tools --script sh
```

Set an environment variable for convenience:
```bash
export SPEC_KIT_SRC=/mnt/c/GitHub/development-spec-kit
uvx --from "$SPEC_KIT_SRC" specify init demo-env --model gpt-4o --ignore-agent-tools --script ps
```

(Optional) Define a shell function:
```bash
specify-dev() { uvx --from /mnt/c/GitHub/development-spec-kit specify "$@"; }
# Then
specify-dev --help
```

## 5. Test script permissions

After running an `init`, check that shell scripts are executable on POSIX systems:

```bash
ls -l scripts | grep .sh
# Expect owner execute bit (e.g. -rwxr-xr-x)
```
On Windows you will instead use the `.ps1` scripts (no chmod needed).

## 6. Run lint / basic checks (add your own)

Currently no enforced lint config is bundled, but you can quickly sanity check importability:
```bash
python -c "import specify_cli; print('Import OK')"
```

## 7. Build a wheel locally (optional)

Validate packaging before publishing:

```bash
uv build
ls dist/
```
Install the built artifact into a fresh throwaway environment if needed.

## 8. Use a temporary workspace

When testing `init --here` in a dirty directory, create a temp workspace:

```bash
mkdir /tmp/spec-test && cd /tmp/spec-test
python -m src.specify_cli init --here --model gpt-4o --ignore-agent-tools --script sh  # if repo copied here
```
Or copy only the modified CLI portion if you want a lighter sandbox.

## 9. Debug network / TLS skips

If you need to bypass TLS validation while experimenting:

```bash
specify check --skip-tls
specify init demo --skip-tls --model gpt-4o --ignore-agent-tools --script ps
```
(Use only for local experimentation.)

## 10. Rapid edit loop summary

| Action | Command |
|--------|---------|
| Run CLI directly | `python -m src.specify_cli --help` |
| Editable install | `uv pip install -e .` then `specify ...` |
| Local uvx run (repo root) | `uvx --from . specify ...` |
| Local uvx run (abs path) | `uvx --from /mnt/c/GitHub/development-spec-kit specify ...` |
| Git branch uvx | `uvx --from git+URL@branch specify ...` |
| Build wheel | `uv build` |

## 11. Clean up

Remove build artifacts / virtual env quickly:
```bash
rm -rf .venv dist build *.egg-info
```

## 12. Common issues

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: typer` | Run `uv pip install -e .` |
| Scripts not executable (Linux) | Re-run init or `chmod +x scripts/*.sh` |
| Git step skipped | You passed `--no-git` or Git not installed |
| Wrong script type downloaded | Pass `--script sh` or `--script ps` explicitly |
| TLS errors on corporate network | Try `--skip-tls` (not for production) |

## 13. Next steps

- Update docs and run through Quick Start using your modified CLI
- Open a PR when satisfied
- (Optional) Tag a release once changes land in `main`

