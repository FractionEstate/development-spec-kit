# FractionEstate Development Spec Kit

Opinionated tooling that makes Spec-Driven Development practical with GitHub Models, GitHub Copilot Chat, and VS Code.

[![Release](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml)
[![Link Checker](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml)

> **Quick jump:** [Overview](docs/overview.md) · [Installation](docs/getting-started/installation.md) · [Quickstart](docs/getting-started/quickstart.md) · [Workflows](docs/workflows.md) · [CLI Reference](docs/reference/cli.md)

## Why Spec Kit exists

Spec Kit trims the distance between intent and implementation. Instead of jumping straight to code, you collaborate with GitHub Copilot Chat—driven by GitHub Models—to produce constitutions, specs, plans, tasks, and finally implementation. The CLI, prompt templates, and documentation keep the workflow reproducible across projects and teams.

Key principles:

- **GitHub Models first** – the CLI only targets GitHub Models; fallback lists and caches revolve around the official catalog.
- **Specs drive code** – prompts and templates reinforce that specifications are the primary artifact.
- **Transparency** – model selections, script flavors, and catalog metadata are stored in `.specify/config/models.json` and surfaced via `specify status`.
- **Toolchain empathy** – Bash and PowerShell scripts ship together, installation scripts print Copilot-centric next steps, and docs mirror what the CLI prints.

## Highlights

- `specify` CLI to scaffold or refresh projects with Copilot-ready prompts.
- Curated `.github/` instructions and `.github/prompts/*.prompt.md` command templates for Copilot Chat.
- `.specify/` scripts and templates that drive clarification, planning, tasking, and implementation flows.
- DocFX documentation describing installation, workflows, references, and troubleshooting.
- GitHub Actions for releases, documentation deployment, and link checking.

## Quick start

```bash
# 1. Install (bash/zsh)
curl -fsSL https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/bash/install-specify.sh | bash

# 2. Scaffold a workspace
specify init my-project --model gpt-4.1

# 3. Inspect configuration
specify status
```

Open the folder in VS Code, launch GitHub Copilot Chat, and run:

1. `/constitution`
2. `/specify`
3. `/clarify`
4. `/plan`
5. `/tasks`
6. `/analyze`
7. `/implement`

Each command writes structured artifacts under `.specify/specs/<feature>/` and respects the constitution.

## CLI essentials

- `specify init` – scaffold or refresh a workspace (supports `--here`, `--model`, `--script`).
- `specify list-models` – view the GitHub Models catalog, including cache age and source.
- `specify status` – summarize prompts, selected model, script flavor, catalog freshness, show a workflow progress dashboard plus feature table, and export the full dataset with `--json`.
- `specify check` – confirm Git, VS Code, and Copilot prerequisites.
- `specify version` – print CLI/Python versions and cache status.

Documentation with full flag descriptions lives in the [CLI reference](docs/reference/cli.md).

## Workspace anatomy

| Path | Purpose |
| ---- | ------- |
| `.specify/` | Memory, scripts, and templates that drive the workflow |
| `.github/` | Copilot instructions, prompts, and GitHub Actions workflows |
| `.vscode/` | Editor settings, tasks, and snippets tuned for Spec-Driven Development |
| `docs/` | DocFX documentation site content |
| `media/` | Brand assets and social preview graphics |

Legacy multi-agent packages remain under `.genreleases/` for archival reference only.

## Documentation

The documentation site is built with DocFX and deployed automatically to GitHub Pages.

- [Overview](docs/overview.md)
- [Installation](docs/getting-started/installation.md)
- [Quickstart](docs/getting-started/quickstart.md)
- [Workflows](docs/workflows.md)
- [Reference guides](docs/reference/cli.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Spec-Driven Development methodology](spec-driven.md)

Run the docs locally:

```bash
cd docs
dotnet tool install -g docfx  # first run only
docfx docfx.json --serve
```

## Contributing & support

- [CONTRIBUTING.md](CONTRIBUTING.md) – development workflow, coding standards, and release process.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) – community expectations.
- [SUPPORT.md](SUPPORT.md) – how to get help.

Bugs, ideas, and questions are welcome in [GitHub Issues](https://github.com/FractionEstate/development-spec-kit/issues/new/choose).

## License

This project is released under the [MIT License](LICENSE).
