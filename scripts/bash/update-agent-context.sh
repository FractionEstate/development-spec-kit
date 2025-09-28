#!/usr/bin/env bash

# Update GitHub Models agent context files with information from plan.md
#
# This script maintains the GitHub Models agent context by parsing feature
# specifications and updating the Copilot guidance file with project
# information.
#
# MAIN FUNCTIONS:
# 1. Environment Validation
#    - Verifies git repository structure and branch information
#    - Checks for required plan.md files and templates
#    - Validates file permissions and accessibility
#
# 2. Plan Data Extraction
#    - Parses plan.md files to extract project metadata
#    - Identifies language/version, frameworks, databases, and project types
#    - Handles missing or incomplete specification data gracefully
#
# 3. Agent File Management
#    - Creates the GitHub Models context file from templates when needed
#    - Updates existing Copilot files with new project information
#    - Preserves manual additions and custom configurations
#
# 4. Content Generation
#    - Generates language-specific build/test commands
#    - Creates appropriate project directory structures
#    - Updates technology stacks and recent changes sections
#    - Maintains consistent formatting and timestamps
#
# 5. GitHub Models Support
#    - Handles GitHub Models-specific file paths and naming conventions
#    - Updates .github/copilot-instructions.md with project information
#    - Optimized for VS Code GitHub Models integration
#
# Usage: ./update-agent-context.sh [copilot]
# Agent types: copilot (only supported agent)
# Leave empty to update existing GitHub Models file if present

set -e

# Enable strict error handling
set -u
set -o pipefail

#==============================================================================
# Configuration and Global Variables
#==============================================================================

# Get script directory and load common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./common.sh
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"

# Get all paths and variables from common functions
eval "$(get_feature_paths)"

NEW_PLAN="$IMPL_PLAN"  # Alias for compatibility with existing code
AGENT_TYPE="${1:-}"

# GitHub Models file path (only supported agent)
COPILOT_FILE="$REPO_ROOT/.github/copilot-instructions.md"

# Template file detection (prefer generated .specify directory, fall back to repository template)
TEMPLATE_CANDIDATES=(
    "$REPO_ROOT/.specify/templates/agent-file-template.md"
    "$REPO_ROOT/templates/agent-file-template.md"
)

TEMPLATE_FILE=""
TEMPLATE_FILE_FOUND="false"

for candidate in "${TEMPLATE_CANDIDATES[@]}"; do
    if [[ -f "$candidate" ]]; then
        TEMPLATE_FILE="$candidate"
        TEMPLATE_FILE_FOUND="true"
        break
    fi
done

if [[ "$TEMPLATE_FILE_FOUND" != "true" ]]; then
    TEMPLATE_FILE="${TEMPLATE_CANDIDATES[0]}"
fi

# Global variables for parsed plan data
NEW_LANG=""
NEW_FRAMEWORK=""
NEW_DB=""
NEW_PROJECT_TYPE=""

#==============================================================================
# Utility Functions
#==============================================================================

log_info() {
    echo "INFO: $1"
}

log_success() {
    echo "✓ $1"
}

log_error() {
    echo "ERROR: $1" >&2
}

log_warning() {
    echo "WARNING: $1" >&2
}

show_usage() {
        local script_name
        script_name=$(basename "${BASH_SOURCE[0]}")

        cat <<EOF
Usage: ./$script_name [copilot]

Refresh the GitHub Models Copilot context by reading plan metadata.

Arguments:
    copilot       Update only the GitHub Models context file.
    -h, --help    Show this help message and exit.

Notes:
    • Run without arguments to refresh all existing GitHub Models context files.
    • Requires a populated feature plan (plan.md) for metadata extraction.
EOF
}

# Cleanup function for temporary files
cleanup() {
    local exit_code=$?
    rm -f /tmp/agent_update_*_$$
    rm -f /tmp/manual_additions_$$
    exit $exit_code
}

# Set up cleanup trap
trap cleanup EXIT INT TERM

#==============================================================================
# Validation Functions
#==============================================================================

validate_environment() {
    # Check if we have a current branch/feature (git or non-git)
    if [[ -z "$CURRENT_BRANCH" ]]; then
        log_error "Unable to determine current feature"
        if [[ "$HAS_GIT" == "true" ]]; then
            log_info "Make sure you're on a feature branch"
        else
            log_info "Set SPECIFY_FEATURE environment variable or create a feature first"
        fi
        exit 1
    fi

    # Check if plan.md exists
    if [[ ! -f "$NEW_PLAN" ]]; then
        log_error "No plan.md found at $NEW_PLAN"
        log_info "Make sure you're working on a feature with a corresponding spec directory"
        if [[ "$HAS_GIT" != "true" ]]; then
            log_info "Use: export SPECIFY_FEATURE=your-feature-name or create a new feature first"
        fi
        exit 1
    fi

    # Check if template exists (needed for new files)
    if [[ "$TEMPLATE_FILE_FOUND" != "true" ]]; then
        log_warning "Agent template not found. Creating new GitHub Models files will fail until a template exists."
        log_warning "Looked for:"
        for candidate in "${TEMPLATE_CANDIDATES[@]}"; do
            log_warning "  - $candidate"
        done
    else
        log_info "Using agent template: $TEMPLATE_FILE"
    fi
}

#==============================================================================
# Plan Parsing Functions
#==============================================================================

extract_plan_field() {
    local field_pattern="$1"
    local plan_file="$2"

    grep "^\*\*${field_pattern}\*\*: " "$plan_file" 2>/dev/null | \
        head -1 | \
        sed "s|^\*\*${field_pattern}\*\*: ||" | \
        sed 's/^[ \t]*//;s/[ \t]*$//' | \
        grep -v "NEEDS CLARIFICATION" | \
        grep -v "^N/A$" || echo ""
}

parse_plan_data() {
    local plan_file="$1"

    if [[ ! -f "$plan_file" ]]; then
        log_error "Plan file not found: $plan_file"
        return 1
    fi

    if [[ ! -r "$plan_file" ]]; then
        log_error "Plan file is not readable: $plan_file"
        return 1
    fi

    log_info "Parsing plan data from $plan_file"

    NEW_LANG=$(extract_plan_field "Language/Version" "$plan_file")
    NEW_FRAMEWORK=$(extract_plan_field "Primary Dependencies" "$plan_file")
    NEW_DB=$(extract_plan_field "Storage" "$plan_file")
    NEW_PROJECT_TYPE=$(extract_plan_field "Project Type" "$plan_file")

    # Log what we found
    if [[ -n "$NEW_LANG" ]]; then
        log_info "Found language: $NEW_LANG"
    else
        log_warning "No language information found in plan"
    fi

    if [[ -n "$NEW_FRAMEWORK" ]]; then
        log_info "Found framework: $NEW_FRAMEWORK"
    fi

    if [[ -n "$NEW_DB" ]] && [[ "$NEW_DB" != "N/A" ]]; then
        log_info "Found database: $NEW_DB"
    fi

    if [[ -n "$NEW_PROJECT_TYPE" ]]; then
        log_info "Found project type: $NEW_PROJECT_TYPE"
    fi
}

format_technology_stack() {
    local lang="$1"
    local framework="$2"
    local parts=()

    # Add non-empty parts
    [[ -n "$lang" && "$lang" != "NEEDS CLARIFICATION" ]] && parts+=("$lang")
    [[ -n "$framework" && "$framework" != "NEEDS CLARIFICATION" && "$framework" != "N/A" ]] && parts+=("$framework")

    # Join with proper formatting
    if [[ ${#parts[@]} -eq 0 ]]; then
        echo ""
    elif [[ ${#parts[@]} -eq 1 ]]; then
        echo "${parts[0]}"
    else
        # Join multiple parts with " + "
        local result="${parts[0]}"
        for ((i=1; i<${#parts[@]}; i++)); do
            result="$result + ${parts[i]}"
        done
        echo "$result"
    fi
}

#==============================================================================
# Template and Content Generation Functions
#==============================================================================

escape_for_sed() {
    local value="$1"
    printf '%s' "$value" | sed 's/[|&]/\\&/g'
}

get_project_structure() {
    local project_type="$1"

    if [[ "$project_type" == *"web"* ]]; then
        printf '%s' "backend/\\nfrontend/\\ntests/"
    else
        printf '%s' "src/\\ntests/"
    fi
}

get_commands_for_language() {
    local lang="$1"

    case "$lang" in
        *"Python"*)
            echo "cd src && pytest && ruff check ."
            ;;
        *"Rust"*)
            echo "cargo test && cargo clippy"
            ;;
        *"JavaScript"*|*"TypeScript"*)
            echo "npm test && npm run lint"
            ;;
        *)
            echo "# Add commands for $lang"
            ;;
    esac
}

get_language_conventions() {
    local lang="$1"
    echo "$lang: Follow standard conventions"
}

create_new_agent_file() {
    local target_file="$1"
    local temp_file="$2"
    local project_name="$3"
    local current_date="$4"

    if [[ ! -f "$TEMPLATE_FILE" ]]; then
        log_error "Template not found at $TEMPLATE_FILE"
        return 1
    fi

    if [[ ! -r "$TEMPLATE_FILE" ]]; then
        log_error "Template file is not readable: $TEMPLATE_FILE"
        return 1
    fi

    log_info "Creating new agent context file from template..."

    if ! cp "$TEMPLATE_FILE" "$temp_file"; then
        log_error "Failed to copy template file"
        return 1
    fi

    # Replace template placeholders
    local project_structure
    project_structure=$(get_project_structure "$NEW_PROJECT_TYPE")
    local commands
    commands=$(get_commands_for_language "$NEW_LANG")
    local language_conventions
    language_conventions=$(get_language_conventions "$NEW_LANG")

    local tech_stack
    if [[ -n "$NEW_LANG" && -n "$NEW_FRAMEWORK" ]]; then
        tech_stack="- $NEW_LANG + $NEW_FRAMEWORK ($CURRENT_BRANCH)"
    elif [[ -n "$NEW_LANG" ]]; then
        tech_stack="- $NEW_LANG ($CURRENT_BRANCH)"
    elif [[ -n "$NEW_FRAMEWORK" ]]; then
        tech_stack="- $NEW_FRAMEWORK ($CURRENT_BRANCH)"
    else
        tech_stack="- ($CURRENT_BRANCH)"
    fi

    local recent_change
    if [[ -n "$NEW_LANG" && -n "$NEW_FRAMEWORK" ]]; then
        recent_change="- $CURRENT_BRANCH: Added $NEW_LANG + $NEW_FRAMEWORK"
    elif [[ -n "$NEW_LANG" ]]; then
        recent_change="- $CURRENT_BRANCH: Added $NEW_LANG"
    elif [[ -n "$NEW_FRAMEWORK" ]]; then
        recent_change="- $CURRENT_BRANCH: Added $NEW_FRAMEWORK"
    else
        recent_change="- $CURRENT_BRANCH: Added"
    fi

    local substitutions=(
        "s|\[PROJECT NAME\]|$(escape_for_sed "$project_name")|"
        "s|\[DATE\]|$(escape_for_sed "$current_date")|"
        "s|\[EXTRACTED FROM ALL PLAN.MD FILES\]|$(escape_for_sed "$tech_stack")|"
        "s|\[ACTUAL STRUCTURE FROM PLANS\]|$(escape_for_sed "$project_structure")|g"
        "s|\[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES\]|$(escape_for_sed "$commands")|"
        "s|\[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE\]|$(escape_for_sed "$language_conventions")|"
        "s|\[LAST 3 FEATURES AND WHAT THEY ADDED\]|$(escape_for_sed "$recent_change")|"
    )

    for substitution in "${substitutions[@]}"; do
        if ! sed -i.bak -e "$substitution" "$temp_file"; then
            log_error "Failed to perform substitution: $substitution"
            rm -f "$temp_file" "$temp_file.bak"
            return 1
        fi
    done

    # Convert \n sequences to actual newlines
    local newline
    newline=$(printf '\n')
    sed -i.bak2 "s/\\\\n/${newline}/g" "$temp_file"

    # Clean up backup files
    rm -f "$temp_file.bak" "$temp_file.bak2"

    return 0
}




update_existing_agent_file() {
    local target_file="$1"
    local current_date="$2"

    log_info "Updating existing agent context file..."

    # Use a single temporary file for atomic update
    local temp_file
    temp_file=$(mktemp) || {
        log_error "Failed to create temporary file"
        return 1
    }

    # Process the file in one pass
    local tech_stack
    tech_stack=$(format_technology_stack "$NEW_LANG" "$NEW_FRAMEWORK")
    local new_tech_entries=()
    local new_change_entry=""

    # Prepare new technology entries
    if [[ -n "$tech_stack" ]] && ! grep -q "$tech_stack" "$target_file"; then
        new_tech_entries+=("- $tech_stack ($CURRENT_BRANCH)")
    fi

    if [[ -n "$NEW_DB" ]] && [[ "$NEW_DB" != "N/A" ]] && [[ "$NEW_DB" != "NEEDS CLARIFICATION" ]] && ! grep -q "$NEW_DB" "$target_file"; then
        new_tech_entries+=("- $NEW_DB ($CURRENT_BRANCH)")
    fi

    # Prepare new change entry
    if [[ -n "$tech_stack" ]]; then
        new_change_entry="- $CURRENT_BRANCH: Added $tech_stack"
    elif [[ -n "$NEW_DB" ]] && [[ "$NEW_DB" != "N/A" ]] && [[ "$NEW_DB" != "NEEDS CLARIFICATION" ]]; then
        new_change_entry="- $CURRENT_BRANCH: Added $NEW_DB"
    fi

    # Process file line by line
    local in_tech_section=false
    local in_changes_section=false
    local tech_entries_added=false
    local existing_changes_count=0

    while IFS= read -r line || [[ -n "$line" ]]; do
        # Handle Active Technologies section
        if [[ "$line" == "## Active Technologies" ]]; then
            echo "$line" >> "$temp_file"
            in_tech_section=true
            continue
        elif [[ $in_tech_section == true ]] && [[ "$line" =~ ^##[[:space:]] ]]; then
            # Add new tech entries before closing the section
            if [[ $tech_entries_added == false ]] && [[ ${#new_tech_entries[@]} -gt 0 ]]; then
                printf '%s\n' "${new_tech_entries[@]}" >> "$temp_file"
                tech_entries_added=true
            fi
            echo "$line" >> "$temp_file"
            in_tech_section=false
            continue
        elif [[ $in_tech_section == true ]] && [[ -z "$line" ]]; then
            # Add new tech entries before empty line in tech section
            if [[ $tech_entries_added == false ]] && [[ ${#new_tech_entries[@]} -gt 0 ]]; then
                printf '%s\n' "${new_tech_entries[@]}" >> "$temp_file"
                tech_entries_added=true
            fi
            echo "$line" >> "$temp_file"
            continue
        fi

        # Handle Recent Changes section
        if [[ "$line" == "## Recent Changes" ]]; then
            echo "$line" >> "$temp_file"
            # Add new change entry right after the heading
            if [[ -n "$new_change_entry" ]]; then
                echo "$new_change_entry" >> "$temp_file"
            fi
            in_changes_section=true
            continue
        elif [[ $in_changes_section == true ]] && [[ "$line" =~ ^##[[:space:]] ]]; then
            echo "$line" >> "$temp_file"
            in_changes_section=false
            continue
        elif [[ $in_changes_section == true ]] && [[ "$line" == "- "* ]]; then
            # Keep only first 2 existing changes
            if [[ $existing_changes_count -lt 2 ]]; then
                echo "$line" >> "$temp_file"
                ((existing_changes_count++))
            fi
            continue
        fi

        # Update timestamp
        if [[ "$line" =~ \*\*Last\ updated\*\*:.*[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] ]]; then
            # shellcheck disable=SC2001
            echo "$line" | sed "s/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/$current_date/" >> "$temp_file"
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$target_file"

    # Post-loop check: if we're still in the Active Technologies section and haven't added new entries
    if [[ $in_tech_section == true ]] && [[ $tech_entries_added == false ]] && [[ ${#new_tech_entries[@]} -gt 0 ]]; then
        printf '%s\n' "${new_tech_entries[@]}" >> "$temp_file"
    fi

    # Move temp file to target atomically
    if ! mv "$temp_file" "$target_file"; then
        log_error "Failed to update target file"
        rm -f "$temp_file"
        return 1
    fi

    return 0
}
#==============================================================================
# Main Agent File Update Function
#==============================================================================

update_agent_file() {
    local target_file="$1"
    local agent_name="$2"

    if [[ -z "$target_file" ]] || [[ -z "$agent_name" ]]; then
        log_error "update_agent_file requires target_file and agent_name parameters"
        return 1
    fi

    log_info "Updating $agent_name context file: $target_file"

    local project_name
    project_name=$(basename "$REPO_ROOT")
    local current_date
    current_date=$(date +%Y-%m-%d)

    # Create directory if it doesn't exist
    local target_dir
    target_dir=$(dirname "$target_file")
    if [[ ! -d "$target_dir" ]]; then
        if ! mkdir -p "$target_dir"; then
            log_error "Failed to create directory: $target_dir"
            return 1
        fi
    fi

    if [[ ! -f "$target_file" ]]; then
        # Create new file from template
        local temp_file
        temp_file=$(mktemp) || {
            log_error "Failed to create temporary file"
            return 1
        }

        if create_new_agent_file "$target_file" "$temp_file" "$project_name" "$current_date"; then
            if mv "$temp_file" "$target_file"; then
                log_success "Created new $agent_name context file"
            else
                log_error "Failed to move temporary file to $target_file"
                rm -f "$temp_file"
                return 1
            fi
        else
            log_error "Failed to create new agent file"
            rm -f "$temp_file"
            return 1
        fi
    else
        # Update existing file
        if [[ ! -r "$target_file" ]]; then
            log_error "Cannot read existing file: $target_file"
            return 1
        fi

        if [[ ! -w "$target_file" ]]; then
            log_error "Cannot write to existing file: $target_file"
            return 1
        fi

        if update_existing_agent_file "$target_file" "$current_date"; then
            log_success "Updated existing $agent_name context file"
        else
            log_error "Failed to update existing agent file"
            return 1
        fi
    fi

    return 0
}

#==============================================================================
# Agent Selection and Processing
#==============================================================================

update_specific_agent() {
    local agent_type="$1"

    case "$agent_type" in
        copilot)
            update_agent_file "$COPILOT_FILE" "GitHub Models"
            ;;
        *)
            log_error "Unknown agent type '$agent_type'"
            log_error "Only 'copilot' is supported for GitHub Models contexts"
            echo
            show_usage
            exit 1
            ;;
    esac
}

update_all_existing_agents() {
    local found_agent=false

    # Check for GitHub Models file and update if it exists
    if [[ -f "$COPILOT_FILE" ]]; then
        update_agent_file "$COPILOT_FILE" "GitHub Models"
        found_agent=true
    fi

    # If no agent files exist, create a default GitHub Models file
    if [[ "$found_agent" == false ]]; then
        log_info "No existing agent files found, creating default GitHub Models file..."
        update_agent_file "$COPILOT_FILE" "GitHub Models"
    fi
}
print_summary() {
    echo
    log_info "Summary of changes:"

    if [[ -n "$NEW_LANG" ]]; then
        echo "  - Added language: $NEW_LANG"
    fi

    if [[ -n "$NEW_FRAMEWORK" ]]; then
        echo "  - Added framework: $NEW_FRAMEWORK"
    fi

    if [[ -n "$NEW_DB" ]] && [[ "$NEW_DB" != "N/A" ]]; then
        echo "  - Added database: $NEW_DB"
    fi

    local metadata_detected="false"
    if [[ -n "$NEW_LANG" || -n "$NEW_FRAMEWORK" ]]; then
        metadata_detected="true"
    elif [[ -n "$NEW_DB" ]] && [[ "$NEW_DB" != "N/A" ]]; then
        metadata_detected="true"
    fi

    if [[ "$metadata_detected" == "false" ]]; then
        echo "  - No new plan metadata detected"
    fi

    if [[ -z "$NEW_LANG" && -z "$NEW_FRAMEWORK" && ( -z "$NEW_DB" || "$NEW_DB" == "N/A" ) ]]; then
        echo "  - No new plan metadata detected"
    fi

    echo
    log_info "Usage tip: $0 [copilot]"
}

#==============================================================================
# Main Execution
#==============================================================================

main() {
    if [[ "$AGENT_TYPE" == "-h" || "$AGENT_TYPE" == "--help" ]]; then
        show_usage
        exit 0
    fi

    # Validate environment before proceeding
    validate_environment

    log_info "=== Updating GitHub Models context for feature $CURRENT_BRANCH ==="

    # Parse the plan file to extract project information
    if ! parse_plan_data "$NEW_PLAN"; then
        log_error "Failed to parse plan data"
        exit 1
    fi

    # Process based on agent type argument
    local success=true

    if [[ -z "$AGENT_TYPE" ]]; then
        # No specific agent provided - update all existing agent files
    log_info "No agent specified, refreshing GitHub Models context..."
        if ! update_all_existing_agents; then
            success=false
        fi
    else
        # Specific agent provided - update only that agent
        log_info "Updating requested agent: $AGENT_TYPE"
        if ! update_specific_agent "$AGENT_TYPE"; then
            success=false
        fi
    fi

    # Print summary
    print_summary

    if [[ "$success" == true ]]; then
        log_success "GitHub Models context update completed successfully"
        exit 0
    else
        log_error "GitHub Models context update completed with errors"
        exit 1
    fi
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
