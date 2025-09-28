#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Spec Kit release archives for the GitHub Copilot workflow templates.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS and/or SCRIPTS env vars to limit what gets built.
#     AGENTS  : space or comma separated subset of: copilot (default: copilot)
#     SCRIPTS : space or comma separated subset of: sh ps (default: both)
#   Examples:
#     AGENTS=copilot SCRIPTS=sh $0 v0.2.0
#     SCRIPTS=ps $0 v0.2.0

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  sed -E \
    -e 's@(/?)memory/@.specify/memory/@g' \
    -e 's@(/?)scripts/@.specify/scripts/@g' \
    -e 's@(/?)templates/@.specify/templates/@g'
}

extract_script_command() {
  local variant=$1
  awk -v sv="$variant" '
    BEGIN { in_block=0 }
    /^<!--[[:space:]]*prompt-scripts/ { in_block=1; next }
    in_block {
      if ($0 ~ /-->[[:space:]]*$/) { in_block=0; exit }
      if ($0 ~ "^[[:space:]]*" sv ":[[:space:]]*") {
        line=$0
        sub(/^[[:space:]]*/, "", line)
        sub(sv ":[[:space:]]*", "", line)
        print line
        exit
      }
      next
    }
  '
}

generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  mkdir -p "$output_dir"
  for template in templates/commands/*.md; do
    [[ -f "$template" ]] || continue
    local name description script_command body
    name=$(basename "$template" .md)

    # Normalize line endings
    file_content=$(tr -d '\r' < "$template")

  # Extract description from YAML frontmatter
    description=$(printf '%s\n' "$file_content" | awk '/^description:/ {sub(/^description:[[:space:]]*/, ""); print; exit}')
  script_command=$(printf '%s\n' "$file_content" | extract_script_command "$script_variant")

    if [[ -z $script_command ]]; then
      echo "Warning: no script command found for $script_variant in $template" >&2
      script_command="(Missing script command for $script_variant)"
    fi

    # Replace {SCRIPT} placeholder with the script command
    body=$(printf '%s\n' "$file_content" | sed "s|{SCRIPT}|${script_command}|g")

    # Remove the prompt-scripts comment block from the distributed prompt
    body=$(printf '%s\n' "$body" | awk '
      /^<!--[[:space:]]*prompt-scripts/ { in_comment=1; next }
      in_comment {
        if ($0 ~ /-->[[:space:]]*$/) { in_comment=0 }
        next
      }
      { print }
    ')

    # Apply other substitutions
    body=$(printf '%s\n' "$body" | sed "s/{ARGS}/$arg_format/g" | sed "s/__AGENT__/$agent/g" | rewrite_paths)

    case $ext in
      toml)
        { echo "description = \"$description\""; echo; echo "prompt = \"\"\""; echo "$body"; echo "\"\"\""; } > "$output_dir/$name.$ext" ;;
      md)
        echo "$body" > "$output_dir/$name.$ext" ;;
      prompt.md)
        echo "$body" > "$output_dir/$name.$ext" ;;
    esac
  done
}

build_variant() {
  local agent=$1 script=$2
  local base_dir="$GENRELEASES_DIR/sdd-${agent}-package-${script}"
  echo "Building $agent ($script) package..."
  mkdir -p "$base_dir"

  # Copy base structure but filter scripts by variant
  SPEC_DIR="$base_dir/.specify"
  mkdir -p "$SPEC_DIR"

  [[ -d memory ]] && { cp -r memory "$SPEC_DIR/"; echo "Copied memory -> .specify"; }

  # Only copy the relevant script variant directory
  if [[ -d scripts ]]; then
    mkdir -p "$SPEC_DIR/scripts"
    case $script in
      sh)
        [[ -d scripts/bash ]] && { cp -r scripts/bash "$SPEC_DIR/scripts/"; echo "Copied scripts/bash -> .specify/scripts"; }
        # Copy any script files that aren't in variant-specific directories
        find scripts -maxdepth 1 -type f -exec cp {} "$SPEC_DIR/scripts/" \; 2>/dev/null || true
        ;;
      ps)
        [[ -d scripts/powershell ]] && { cp -r scripts/powershell "$SPEC_DIR/scripts/"; echo "Copied scripts/powershell -> .specify/scripts"; }
        # Copy any script files that aren't in variant-specific directories
        find scripts -maxdepth 1 -type f -exec cp {} "$SPEC_DIR/scripts/" \; 2>/dev/null || true
        ;;
    esac
  fi

  [[ -d templates ]] && { mkdir -p "$SPEC_DIR/templates"; find templates -type f -not -path "templates/commands/*" -exec cp --parents {} "$SPEC_DIR"/ \; ; echo "Copied templates -> .specify/templates"; }

  # Copy VSCode configuration for Copilot projects
  if [[ "$agent" == "copilot" && -d templates/.vscode ]]; then
    cp -r templates/.vscode "$base_dir/"
    echo "Copied .vscode configuration for Copilot optimization"
  fi
  # Inject variant into plan-template.md within .specify/templates if present
  local plan_tpl="$base_dir/.specify/templates/plan-template.md"
  if [[ -f "$plan_tpl" ]]; then
    plan_norm=$(tr -d '\r' < "$plan_tpl")
    # Extract script command from YAML frontmatter
  script_command=$(printf '%s\n' "$plan_norm" | extract_script_command "$script")
    if [[ -n $script_command ]]; then
      # Always prefix with .specify/ for plan usage
      script_command=".specify/$script_command"
      # Replace {SCRIPT} placeholder with the script command and __AGENT__ with agent name
      substituted=$(sed "s|{SCRIPT}|${script_command}|g" "$plan_tpl" | tr -d '\r' | sed "s|__AGENT__|${agent}|g")
      # Strip YAML frontmatter from plan template output (keep body only)
      stripped=$(printf '%s\n' "$substituted" | awk 'BEGIN{fm=0;dash=0} /^---$/ {dash++; if(dash==1){fm=1; next} else if(dash==2){fm=0; next}} {if(!fm) print}')
      printf '%s\n' "$stripped" > "$plan_tpl"
    else
      echo "Warning: no plan-template script command found for $script in YAML frontmatter" >&2
    fi
  fi
  # NOTE: We substitute {ARGS} internally. Outward tokens differ intentionally:
  #   * Markdown/prompt (copilot): $ARGUMENTS
  #   * TOML variants are no longer produced in the GitHub Models-only workflow.
  # This keeps formats readable without extra abstraction.

  case $agent in
    copilot)
      mkdir -p "$base_dir/.github/prompts"
      generate_commands copilot prompt.md "\$ARGUMENTS" "$base_dir/.github/prompts" "$script"
      # Copy enhanced Copilot instructions and context files for VSCode Chat optimization
      [[ -f templates/.github/copilot-instructions.md ]] && cp templates/.github/copilot-instructions.md "$base_dir/.github/copilot-instructions.md"
      [[ -f templates/.github/copilot-context.md ]] && cp templates/.github/copilot-context.md "$base_dir/.github/copilot-context.md"
      [[ -f templates/.github/copilot-references.md ]] && cp templates/.github/copilot-references.md "$base_dir/.github/copilot-references.md" ;;
    *)
      echo "Error: Unsupported agent '$agent'. Only 'copilot' is supported." >&2
      exit 1 ;;
  esac
  ( cd "$base_dir" && zip -r "../spec-kit-template-${agent}-${script}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/spec-kit-template-${agent}-${script}-${NEW_VERSION}.zip"
}

# Determine agent list - GitHub Copilot only
ALL_AGENTS=(copilot)
ALL_SCRIPTS=(sh ps)


norm_list() {
  # convert comma+space separated -> space separated unique while preserving order of first occurrence
  tr ',\n' '  ' | awk '{for(i=1;i<=NF;i++){if(!seen[$i]++){printf((out?" ":"") $i)}}}END{printf("\n")}'
}

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=("$@")
  local ok=1
  for it in "${items[@]}"; do
    local found=0
    for a in "${allowed[@]}"; do [[ $it == "$a" ]] && { found=1; break; }; done
    if [[ $found -eq 0 ]]; then
      echo "Error: unknown $type '$it' (allowed: ${allowed[*]})" >&2
      ok=0
    fi
  done
  return $ok
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' "$AGENTS" | norm_list)
  validate_subset agent ALL_AGENTS "${AGENT_LIST[@]}" || exit 1
else
  AGENT_LIST=("${ALL_AGENTS[@]}")
fi

if [[ -n ${SCRIPTS:-} ]]; then
  mapfile -t SCRIPT_LIST < <(printf '%s' "$SCRIPTS" | norm_list)
  validate_subset script ALL_SCRIPTS "${SCRIPT_LIST[@]}" || exit 1
else
  SCRIPT_LIST=("${ALL_SCRIPTS[@]}")
fi

echo "Agents: ${AGENT_LIST[*]}"
echo "Scripts: ${SCRIPT_LIST[*]}"

for agent in "${AGENT_LIST[@]}"; do
  for script in "${SCRIPT_LIST[@]}"; do
    build_variant "$agent" "$script"
  done
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/spec-kit-template-*-"${NEW_VERSION}".zip
