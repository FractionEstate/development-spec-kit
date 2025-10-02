# Local development

This guide shows how to iterate on the Specify CLI, regenerate documentation, and validate changes before opening a pull request.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (installed automatically by the project scripts)
- Git
- Optional: VS Code with GitHub Copilot access to GitHub Models

## 1. Clone and branch

```bash
git clone https://github.com/FractionEstate/development-spec-kit.git
cd development-spec-kit
git checkout -b feature/my-change
```

## 2. Run the CLI straight from source

Use the module entry point for the fastest feedback loop:

```bash
python -m src.specify_cli --help
python -m src.specify_cli list-models --no-cache
python -m src.specify_cli init demo --model gpt-4.1 --ignore-agent-tools
```

You can also invoke the script file directly:

```bash
python src/specify_cli/__init__.py status
```

## 3. Editable install (uv)

```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
uv pip install -e .

specify --help
specify status
```

Editable mode allows you to modify the CLI and re-run commands without reinstalling.

## 4. Exercise real templates with `uvx`

`uvx` lets you run the current repository as if it were a published package:

```bash
uvx --from . specify init demo-uvx --model gpt-4.1 --ignore-agent-tools
```

You can target a remote branch once pushed:

```bash
git push origin feature/my-change
uvx --from git+https://github.com/FractionEstate/development-spec-kit.git@feature/my-change specify list-models --refresh
```

## 5. Validate code changes

- **Syntax check** – `python -m compileall src/specify_cli/__init__.py`
- **Run key commands** – `specify status`, `specify list-models --refresh`, `specify init --here --ignore-agent-tools`
- **Ensure script mapping** – run both `.specify/scripts/bash/*.sh` and `.specify/scripts/powershell/*.ps1` if you changed command templates.

## 6. Update documentation

1. Edit Markdown under `docs/` or the root `README.md`.
2. Preview with DocFX:

   ```bash
   cd docs
   dotnet tool install -g docfx  # first time only
   docfx docfx.json --serve
   ```

3. Visit `http://localhost:8080` to review the site.
4. Run `specify status` and capture new behaviors in the docs if the CLI output changed.

## 7. Build artifacts (optional)

```bash
uv build
ls dist/
```

Install the resulting wheel in a fresh environment when you need to validate packaging.

## 8. Keep things tidy

```bash
rm -rf .venv dist build *.egg-info
```

## 9. Preparing a pull request

- Run through the [Quickstart](getting-started/quickstart.md) with your local CLI to ensure the workflow still works end-to-end.
- Update [CHANGELOG.md](../CHANGELOG.md) under “Unreleased” with a concise summary of your changes.
- Verify docs and README point to the new behavior.
- Push your branch and open a PR. The link checker and documentation workflows run automatically.

## 10. Release workflow (maintainers)

1. Update the changelog and bump the version in `pyproject.toml`.
2. Create a release branch and run `uv build` to ensure packaging passes.
3. Use the `release.yml` GitHub Action to publish artifacts and documentation.
4. Tag the release and announce changes.

## Useful snippets

| Task | Command |
| ---- | ------- |
| Run CLI without install | `python -m src.specify_cli --help` |
| Editable install | `uv pip install -e .` |
| Local `uvx` run | `uvx --from . specify status` |
| Remote branch `uvx` | `uvx --from git+https://github.com/FractionEstate/development-spec-kit.git@branch specify ...` |
| Build wheel | `uv build` |
| Clean artefacts | `rm -rf .venv dist build *.egg-info` |
