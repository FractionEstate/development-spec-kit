# Update Specify Command

---

description: Update an existing feature specification with new requirements or changes.

---

<!-- prompt-scripts
sh: scripts/bash/check-prerequisites.sh --json --paths-only
ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly

-->

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

You are updating an existing feature specification. This command is for modifying a spec that has already been created.

Follow this execution flow:

1. Run `{SCRIPT}` from repo root and parse JSON for FEATURE_DIR and FEATURE_SPEC paths.

2. Load the current specification and show the user:
   - Current feature overview
   - Key requirements summary
   - Last modified date
   - Any existing clarifications

3. Based on user input, identify what needs to be updated:
   - New requirements to add
   - Existing requirements to modify or remove
   - User stories changes
   - Success criteria updates
   - Dependency changes

4. Update the specification file with:
   - Preserved existing content unless explicitly changed
   - New `[NEEDS CLARIFICATION: ...]` markers for ambiguous changes
   - Updated clarifications section with new questions
   - Maintained section structure and formatting

5. If significant changes are made, check for impact on related files:
   - Review plan.md if it exists (may need updates)
   - Review tasks.md if it exists (may need regeneration)
   - Flag any implementation files that may be affected

6. End your response with a Markdown summary that includes:
   - Updated spec path and change summary
   - New or modified requirements overview
   - Outstanding clarifications (if any)
   - Impact assessment on downstream artifacts
   - A ready-to-copy `@workspace` prompt for `/plan` or `/clarify`
   - Recommended next command

This command preserves existing work while incorporating new requirements. For creating a completely new specification, use `/specify` instead.
