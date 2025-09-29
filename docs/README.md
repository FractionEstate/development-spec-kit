# Documentation

Source for the public docs site, built with [DocFX](https://dotnet.github.io/docfx/).

## Build locally

Prerequisites:
- .NET SDK (for DocFX global tool)

Steps:
1. Install DocFX:
   ```bash
   dotnet tool install -g docfx
   ```
2. Build and serve:
   ```bash
   cd docs
   docfx docfx.json --serve
   ```
3. Open `http://localhost:8080`

## Structure

- `docfx.json` – DocFX configuration
- `index.md` – Docs homepage
- `installation.md` – Installation guide
- `quickstart.md` – Quickstart guide
- `local-development.md` – Contributing locally to the CLI
- `toc.yml` – Table of contents

## Deployment

Docs are built and deployed to GitHub Pages via the "Deploy Documentation to Pages" workflow on pushes to `main`.
