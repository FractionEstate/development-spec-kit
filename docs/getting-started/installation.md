# Installation

Get the Specify CLI running locally so you can bootstrap GitHub Models–ready workspaces in minutes.

## Prerequisites

- **Git** 2.40 or newer
- **Python** 3.11 or newer (the CLI is packaged as a uv tool)
- **curl** (for the POSIX installer) or **Invoke-WebRequest** (for PowerShell)
- A GitHub account with access to GitHub Models (for private models, you will need a token)

> ℹ️ The installer automatically installs [uv](https://docs.astral.sh/uv/) if it is missing and adds it to your `PATH`.

## One-line install (recommended)

Choose the script that matches your shell. Both scripts install or upgrade the CLI and print the next steps for GitHub Copilot Chat.

### POSIX shells (bash/zsh/fish)

```bash
curl -fsSL https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/bash/install-specify.sh | bash

```text

### PowerShell (Windows, macOS, or Linux)

```powershell
iwr https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/powershell/install-specify.ps1 -UseBasicParsing | iex

```text

## Manual installation with uv

If you prefer to manage tools manually or to pin to a branch, install directly with uv:

```bash
uv tool install specify-cli --from git+https://github.com/FractionEstate/development-spec-kit.git

```text

Upgrade to the latest release at any time with:

```bash
uv tool upgrade specify-cli

```text

Remove the tool when you are done experimenting:

```bash
uv tool uninstall specify-cli

```text

## Verify your setup

```bash
specify version
specify check

```text

`specify version` prints the CLI version, Python runtime, platform, and cache status. `specify check` confirms Git, VS Code, and GitHub Models prerequisites.

## GitHub Models access

- Public models require no authentication.
- Private or preview models require a token. Pass it with `--github-token`, or export `GH_TOKEN` / `GITHUB_TOKEN` before running `specify init` or `specify list-models`.
- The CLI caches the catalog for one hour. Refresh it at any time with `specify list-models --refresh`.

## What’s next

1. Walk through the [Quickstart](quickstart.md) to initialize your first workspace.
2. Review the [workflows guide](../workflows.md) to see how each Copilot command fits into Spec-Driven Development.
3. Explore the [CLI reference](../reference/cli.md) for additional commands and flags.
