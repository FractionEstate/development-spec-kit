# Documentation

Source for the public documentation site, built with [DocFX](https://dotnet.github.io/docfx/).

## Build locally

Prerequisite: .NET SDK (for the DocFX global tool).

```bash
dotnet tool install -g docfx
cd docs
docfx docfx.json --serve
```

Open `http://localhost:8080` to preview the site.

## Structure

- `index.md` – Documentation hub
- `overview.md` – Toolkit philosophy and key components
- `getting-started/` – Installation and quickstart guides
- `workflows.md` – Slash-command lifecycle walkthrough
- `reference/` – CLI, script, and configuration references
- `troubleshooting.md` – Common issues and fixes
- `local-development.md` – How to hack on the CLI
- `toc.yml` – Site navigation

## Deployment

`docs.yml` GitHub Actions workflow builds and publishes `_site/` to GitHub Pages on pushes to `main`.
