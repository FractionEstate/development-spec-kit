---
description: Resume or modify implementation execution with the current task status and any changes.
---

<!-- prompt-scripts
sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
-->

The user input can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

You are resuming or updating an existing implementation. This command is for continuing development work or making changes to ongoing implementation.

Follow this execution flow:

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list.

2. Load and analyze current implementation state:
   - **REQUIRED**: Read tasks.md for task list and completion status
   - **REQUIRED**: Read plan.md for technical context
   - **Current progress**: Identify completed tasks [X] vs remaining tasks
   - **Available artifacts**: Check for data-model.md, contracts/, research.md, quickstart.md
   - **Existing code**: Review any implemented features or tests

3. Assess what needs to be updated based on user input:
   - Resume from where implementation left off
   - Modify existing implementation based on new requirements
   - Fix issues or bugs in completed tasks
   - Adjust approach based on lessons learned
   - Handle blocking dependencies that have been resolved

4. Continue implementation execution following the task plan:
   - **Skip completed tasks**: Don't redo tasks marked [X]
   - **Resume in-progress**: Continue any partially completed work
   - **Respect dependencies**: Maintain proper task ordering
   - **Update approach**: Incorporate any implementation feedback or changes
   - **Handle conflicts**: Resolve any conflicts with existing code

5. Implementation execution rules (adapted for updates):
   - Preserve existing working code unless explicitly changing it
   - Update tests when modifying functionality
   - Maintain consistency with completed work
   - Follow established patterns and architecture
   - Document significant changes or deviations

6. Progress tracking with preservation:
   - Keep completed tasks marked as [X]
   - Mark newly completed tasks as [X] in tasks.md
   - Report progress after each task completion
   - Handle failures gracefully without breaking completed work
   - Provide clear error context for debugging

7. Completion validation:
   - Verify new work integrates with existing implementation
   - Check that tests still pass after changes
   - Confirm implementation still matches original specification
   - Validate that modifications don't break completed features

8. Deliver your final response as a Markdown summary that includes:
   - Branch name and implementation status
   - Files modified with absolute paths (new and updated)
   - Task completion progress (X completed out of Y total)
   - Test/validation outcomes with specific results
   - Any issues encountered and their resolution
   - Integration notes for modified vs existing code
   - A ready-to-copy `@workspace` prompt for validation or further work
   - Recommended next command

This command preserves existing implementation work while making necessary updates or continuing incomplete work. For starting fresh implementation, use `/implement` instead.
