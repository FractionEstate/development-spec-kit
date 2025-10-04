# Update Tasks Command

---

description: Update the task breakdown with new development steps or priority changes.

---

<!-- prompt-scripts
sh: scripts/bash/check-prerequisites.sh --json
ps: scripts/powershell/check-prerequisites.ps1 -Json

-->

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

You are updating an existing task breakdown. This command is for modifying development tasks based on plan changes or progress updates.

Follow this execution flow:

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list.

2. Load and analyze current state:
   - Existing tasks.md with current task breakdown
   - Updated plan.md and design documents
   - Any completed tasks (marked with [X])
   - Current implementation progress

3. Identify what needs to be updated based on user input:
   - New tasks from plan changes
   - Modified task priorities or dependencies
   - Removal of obsolete tasks
   - Task splitting or merging
   - Parallel execution changes

4. Update the task breakdown with:
   - Preserved completed tasks ([X] marked)
   - New tasks from updated requirements or design
   - Revised task dependencies and ordering
   - Updated parallel execution markers [P]
   - Adjusted task descriptions for clarity

5. Maintain task generation rules:
   - Each new contract → new contract test task [P]
   - Each new entity → new model creation task [P]
   - Modified dependencies → updated task ordering
   - Same file modifications → sequential tasks (no [P])
   - Different files → parallel tasks [P]

6. Ensure proper task organization:
   - Setup tasks first
   - Tests before implementation (TDD approach)
   - Core development in dependency order
   - Integration tasks after core features
   - Polish and validation tasks last

7. Create updated FEATURE_DIR/tasks.md preserving:
   - Completed task status
   - Task numbering continuity
   - Clear file paths and dependencies
   - Parallel execution guidance

8. End with a Markdown summary that calls out:
   - Branch and task file status
   - Number of new, modified, and preserved tasks
   - Key dependency changes or priority shifts
   - Completion progress (X completed out of Y total)
   - A ready-to-copy `@workspace` prompt for `/implement`
   - Recommended next command

This command preserves implementation progress while adapting to plan changes. For creating a fresh task breakdown, use `/tasks` instead.
