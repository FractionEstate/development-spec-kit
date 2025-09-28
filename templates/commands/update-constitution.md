---
description: Update existing project constitution with new principles or governance changes.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

You are updating an existing project constitution at `/memory/constitution.md`. This command is for making changes to a constitution that has already been established.

Follow this execution flow:

1. Load the current constitution at `/memory/constitution.md` and display its current version and key principles to the user.

2. Identify what needs to be updated based on user input:
   - New principles to add
   - Existing principles to modify or remove
   - Governance changes
   - Version updates

3. Follow the same constitution update workflow as `/constitution` but with emphasis on:
   - Preserving existing principles unless explicitly changed
   - Proper version bumping (MAJOR for breaking changes, MINOR for additions, PATCH for clarifications)
   - Impact analysis on existing specs and plans
   - Migration guidance if principles change significantly

4. Before making changes, show the user:
   - Current constitution summary
   - Proposed changes
   - Version bump rationale
   - Files that may need updates due to changes

5. After confirmation, execute the full constitution update workflow.

6. Output a final summary with:
   - Version change details (old → new)
   - Summary of changes made
   - Files flagged for review/update
   - A ready-to-copy `@workspace` prompt for reviewing affected files
   - Suggested commit message

This command is specifically for updating existing constitutions. For creating a new constitution from scratch, use `/constitution` instead.
