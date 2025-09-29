#!/usr/bin/env pwsh
<#!
.SYNOPSIS
  Easy installer/manager for the FractionEstate Specify CLI using uv (PowerShell)

.DESCRIPTION
  Installs, updates, or uninstalls the specify-cli uv tool. Installs uv automatically if it's missing.

.PARAMETER Update
  Upgrade to the latest version

.PARAMETER Uninstall
  Remove the installed CLI

.PARAMETER From
  Override install source (default: git+https://github.com/FractionEstate/development-spec-kit.git)

.EXAMPLE
  # Install
  iwr https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/powershell/install-specify.ps1 -UseBasicParsing | iex

.EXAMPLE
  # Update
  ./scripts/powershell/install-specify.ps1 -Update

.EXAMPLE
  # Uninstall
  ./scripts/powershell/install-specify.ps1 -Uninstall
#>

param(
  [switch]$Update,
  [switch]$Uninstall,
  [string]$From = 'git+https://github.com/FractionEstate/development-spec-kit.git'
)

function Require-Cmd {
  param([string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: '$Name' is required but not found in PATH."
    exit 1
  }
}

function Ensure-Uv {
  if (Get-Command uv -ErrorAction SilentlyContinue) {
    return
  }

  Write-Host "uv not found. Installing uv..."
  $env:PATH = "$env:USERPROFILE\.local\bin;$env:LOCALAPPDATA\Programs\uv;$env:USERPROFILE\AppData\Roaming\uv\bin;$env:PATH"
  $installScript = Invoke-WebRequest https://astral.sh/uv/install.ps1 -UseBasicParsing
  Invoke-Expression $installScript.Content
  $env:PATH = "$env:USERPROFILE\.local\bin;$env:LOCALAPPDATA\Programs\uv;$env:USERPROFILE\AppData\Roaming\uv\bin;$env:PATH"

  if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: uv installation attempted but 'uv' is still not available. Please ensure %USERPROFILE%\\.local\\bin is in PATH and retry."
    exit 1
  }
}

function Install-Specify {
  Write-Host "Installing Specify CLI from: $From"
  uv tool install specify-cli --from $From
  Write-Host "`nInstalled tools:"
  uv tool list | Select-String '^specify-cli' | ForEach-Object { $_.Line }
  Write-Host "Done. Try: specify --help"
}

function Update-Specify {
  Write-Host "Upgrading Specify CLI..."
  uv tool upgrade specify-cli
  Write-Host "`nInstalled tools:"
  uv tool list | Select-String '^specify-cli' | ForEach-Object { $_.Line }
}

function Uninstall-Specify {
  Write-Host "Uninstalling Specify CLI..."
  uv tool uninstall specify-cli
}

# Pre-req checks
Require-Cmd python3
Require-Cmd git
Ensure-Uv

if ($Uninstall) {
  Uninstall-Specify
} elseif ($Update) {
  Update-Specify
} else {
  Install-Specify
}
