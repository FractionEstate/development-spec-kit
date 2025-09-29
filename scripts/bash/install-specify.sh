#!/usr/bin/env bash
set -euo pipefail

# install-specify.sh
# Easy installer/manager for the FractionEstate Specify CLI using uv
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/bash/install-specify.sh | bash
#   # or clone and run locally
#   scripts/bash/install-specify.sh [--update|--uninstall]
#
# Options:
#   --update     Upgrade to the latest version
#   --uninstall  Remove the installed CLI
#   --from <src> Override install source (default: git+https://github.com/FractionEstate/development-spec-kit.git)
#   --help/-h    Show help
#
# Notes:
# - Requires: bash, git, python3.11+, and uv (https://docs.astral.sh/uv/)
# - Installs as a uv tool named 'specify-cli'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

DEFAULT_SRC="git+https://github.com/FractionEstate/development-spec-kit.git"
SRC="$DEFAULT_SRC"
ACTION="install"

print_help() {
  sed -n '1,40p' "$0" | sed 's/^# \{0,1\}//'
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "ERROR: '$1' is required but not found in PATH." >&2; exit 1; }
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --update) ACTION="update"; shift;;
      --uninstall) ACTION="uninstall"; shift;;
      --from) SRC="$2"; shift 2;;
      --help|-h) print_help; exit 0;;
      *) echo "Unknown argument: $1" >&2; print_help; exit 1;;
    esac
  done
}

install() {
  echo "Installing Specify CLI from: $SRC"
  uv tool install specify-cli --from "$SRC"
  echo
  echo "Installed tools:"; uv tool list | grep -E '^specify-cli'
  echo "Done. Try: specify --help"
}

update() {
  echo "Upgrading Specify CLI..."
  uv tool upgrade specify-cli
  echo
  echo "Installed tools:"; uv tool list | grep -E '^specify-cli'
}

uninstall() {
  echo "Uninstalling Specify CLI..."
  uv tool uninstall specify-cli || true
}

main() {
  parse_args "$@"
  # Basic prereq checks
  require_cmd python3
  require_cmd uv
  require_cmd git

  case "$ACTION" in
    install) install;;
    update) update;;
    uninstall) uninstall;;
    *) echo "Unknown action: $ACTION"; exit 1;;
  esac
}

main "$@"
