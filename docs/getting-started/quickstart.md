# Quickstart

Launch a Spec Kit workspace, connect GitHub Copilot Chat, and generate your first specification in under 10 minutes.

## 1. Install the CLI

Follow the [installation guide](installation.md) to install `specify` with a single command.

## 2. Initialize a workspace

Pick a directory name and let the CLI scaffold everything for GitHub Models + VS Code.

```bash
specify init my-first-spec --model gpt-4.1
```

During initialization you will:

1. Select a script flavor (bash or PowerShell).
2. Optionally pick a GitHub Model from the live catalog.
3. Receive next-step instructions tailored for GitHub Copilot Chat.

> Need to work in the current directory? Use `specify init --here` (add `--force` to merge into non-empty directories).

## 3. Open VS Code and load Copilot Chat

```bash
code my-first-spec
```

Inside VS Code:

- Ensure the GitHub Copilot Chat panel is visible.
- Glance through `.github/copilot-instructions.md` for the project briefing.
- Review `.specify/templates` to understand the generated artifacts.

## 4. Run the core workflow commands

Use GitHub Copilot Chat slash commands from the project root:

1. `/constitution` – establish the project principles.
2. `/specify` – capture the feature requirements and user stories.
3. `/clarify` – resolve gaps before planning.
4. `/plan` – produce the technical blueprint.
5. `/tasks` – derive the execution plan.
6. `/analyze` (optional) – cross-check coverage.
7. `/implement` – let Copilot work through the tasks.

Each command writes to `.specify/` and keeps the artifacts synchronized with the constitution.

## 5. Check project status

```bash
specify status
```

The status command confirms:

- Current directory and Git initialization.
- Installed prompt commands under `.github/prompts/`.
- Selected GitHub Model (with when it was set and which catalog source supplied it).
- Script flavor (bash or PowerShell) wired into generated prompts.
- Age of the cached GitHub Models catalog.
- A workflow dashboard that shows which stages (constitution → spec → plan → tasks) are complete and surfaces the next recommended slash commands.
- A feature progress table covering the first few specs with stage checkmarks and suggested next actions (use `specify status --json` to export the full dataset).

## 6. Iterate with confidence

- Regenerate the catalog at any time: `specify list-models --refresh`.
- Update a workspace with fresh prompts or instructions by rerunning `specify init --here`.
- Keep documentation open (Command Palette → `Tasks: Run Task` → `Open Docs Site`) for live previews.

## 7. Keep exploring

- Read the [workflows guide](../workflows.md) for deep dives on each slash command.
- Review [Spec-Driven Development](../../spec-driven.md) to understand the methodology behind the kit.
- Contribute improvements with the [local development guide](../local-development.md).
