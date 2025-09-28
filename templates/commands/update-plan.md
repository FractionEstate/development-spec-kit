---
description: Update the technical implementation plan with architecture or design changes.
---

<!-- prompt-scripts
sh: scripts/bash/check-prerequisites.sh --json
ps: scripts/powershell/check-prerequisites.ps1 -Json
-->

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

You are updating an existing implementation plan. This command is for modifying technical architecture and design decisions.

Follow this execution flow:

1. Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH paths.

2. Load and analyze existing artifacts:
   - Current plan.md with architecture decisions
   - Related design documents (data-model.md, contracts/, etc.)
   - Current specification to understand any requirement changes

3. Identify what needs to be updated based on user input:
   - Architecture changes (technology stack, patterns, libraries)
   - Data model modifications
   - API contract changes
   - New technical constraints or dependencies
   - Performance or security requirement changes

4. Update the implementation plan with:
   - Revised technical approach
   - Updated architecture diagrams or descriptions
   - Modified technology choices with rationale
   - Impact analysis on existing design artifacts
   - Migration strategy if breaking changes are introduced

5. Update related design artifacts as needed:
   - Regenerate data-model.md if entity changes
   - Update contracts/ if API changes
   - Refresh quickstart.md if user flows change
   - Update research.md with new technical decisions

6. Before finalizing, check for downstream impact:
   - Review tasks.md if it exists (may need regeneration)
   - Identify implementation files that may need refactoring
   - Flag potential breaking changes

7. Report results using a Markdown summary that:
   - States the updated plan status and key changes
   - Lists modified design artifacts with absolute paths
   - Highlights architectural decisions and their rationale
   - Notes any breaking changes or migration needs
   - Includes a ready-to-copy `@workspace` prompt for `/tasks` or further planning
   - Recommends the next command (usually `/tasks` to regenerate task breakdown)

This command preserves existing technical decisions while incorporating necessary changes. For creating a plan from scratch, use `/plan` instead.
