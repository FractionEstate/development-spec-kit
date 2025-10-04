# Script reference

Slash commands rely on helper scripts stored in `.specify/scripts/`. Each script has a Bash (`.sh`) and PowerShell (`.ps1`) variant with identical behavior. The CLI wires command templates to the correct script flavor when you run `specify init`.

## Layout

```text
.specify/scripts/
├── bash/
│   ├── check-prerequisites.sh
│   ├── common.sh
│   ├── create-new-feature.sh
│   ├── install-specify.sh
│   ├── setup-plan.sh
│   └── update-agent-context.sh
└── powershell/
    ├── check-prerequisites.ps1
    ├── common.ps1
    ├── create-new-feature.ps1
    ├── install-specify.ps1
    ├── setup-plan.ps1
    └── update-agent-context.ps1

```text

## Core scripts

| Script | Purpose |
| ------ | ------- |
| `check-prerequisites.*` | Verifies that constitution/spec/plan/tasks exist and gathers feature metadata for prompts. |
| `create-new-feature.*` | Allocates the next feature ID, creates directories, and prepares templates. |
| `setup-plan.*` | Populates plan templates with context extracted from the spec. |
| `update-agent-context.*` | Refreshes Copilot instruction files when specs evolve. |
| `install-specify.*` | Convenience installer invoked from the Quickstart documentation. |
| `common.*` | Shared library functions sourced by other scripts. |

## Running scripts manually

Scripts live in `.specify/scripts/<flavor>/`. Invoke them directly when debugging or extending the workflow:

```bash

# Bash example

.specify/scripts/bash/check-prerequisites.sh --json

# PowerShell example

.specify/scripts/powershell/check-prerequisites.ps1 -Json

```text

All scripts are designed to be idempotent and safe to rerun. They emit structured JSON when invoked with `--json`/`-Json`, making it easy to pipe into other tooling.

## Extending the toolkit

1. Add your script to both `bash/` and `powershell/` to preserve parity.
2. Update the relevant command template in `.specify/templates/commands/` to reference the new script.
3. Regenerate the workspace (`specify init --here`) or distribute an updated release so downstream projects receive the new behavior.
