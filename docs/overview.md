# Spec Kit Overview

FractionEstate's Development Spec Kit packages an opinionated workflow for Spec-Driven Development powered by GitHub Models and VS Code. The toolkit combines a CLI, curated Copilot instructions, command templates, and project scaffolding so your specs remain the primary artifact while code becomes a reproducible output.

## What the kit provides

- **CLI automation (`specify`)** – bootstraps new workspaces, manages GitHub Model selection, and keeps prompts/scripts synchronized.
- **Copilot Chat guidance** – `.github/copilot-instructions.md`, `.github/copilot-context.md`, and a library of prompt templates optimized for the slash-command flow.
- **Spec templates** – opinionated markdown blueprints for specs, plans, tasks, research, and constitutions.
- **Script helpers** – Bash and PowerShell automation for prerequisite checks, plan setup, and agent context updates.
- **Documentation & workflows** – detailed guides that connect each Copilot command to tangible artifacts and quality gates.

## Design principles

1. **GitHub Models first** – the CLI only targets GitHub Models; fallbacks and cache metadata revolve around the GitHub catalog.
2. **Spec before code** – every prompt and template reinforces that specifications, plans, and tasks lead implementation.
3. **Transparency** – generated code, model choices, and script flavors are persisted in `.specify/config` and surfaced via `specify status`.
4. **Toolchain empathy** – Bash/PowerShell scripts mirror each other, commands print actionable next steps, and documentation links match the command outputs.
5. **Focused surface area** – only the commands and files required for the workflow ship in the template; legacy agents and extraneous prompts live under `.genreleases/` for archive purposes.

## Key components in a generated workspace

| Path | Purpose |
| ---- | ------- |
| `.specify/` | Memory, scripts, and templates that power the AI workflows |
| `.github/` | Copilot Chat instructions, context, prompts, and GitHub workflows |
| `.vscode/` | Tasks, settings, and snippets optimized for Spec-Driven Development |
| `docs/` | DocFX documentation describing the methodology and workflow |
| `media/` | Brand assets used in README and docs |

## Lifecycle at a glance

1. **Scaffold** – run `specify init` to download the template, pick a GitHub Model, and set the script flavor.
2. **Specify** – collaborate with Copilot Chat through `/constitution`, `/specify`, `/clarify`.
3. **Plan** – create implementation plans, tasks, and analyze them for consistency.
4. **Implement** – let `/implement` orchestrate tasks, then iterate on the artifacts as requirements evolve.
5. **Sustain** – use `specify status` and documentation to keep the workspace aligned and ready for future regenerations.

## Related reading

- [Quickstart](getting-started/quickstart.md)
- [Workflows guide](workflows.md)
- [CLI reference](reference/cli.md)
- [Spec-Driven Development methodology](../spec-driven.md)
