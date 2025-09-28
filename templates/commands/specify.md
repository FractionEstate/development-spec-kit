---
description: Turn your feature idea into a detailed specification document with requirements and user stories.
---

<!-- prompt-scripts
sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
-->

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for BRANCH_NAME and SPEC_FILE. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load `templates/spec-template.md` to understand required sections.
3. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings. Mark any unknowns with `[NEEDS CLARIFICATION: ...]` and populate the `## Clarifications` section.
4. End your response with a Markdown summary that lists: spec path, feature overview, outstanding clarifications (or `None`), key decision notes, a ready-to-use `@workspace` prompt for `/clarify` or `/plan`, and the recommended next command.

Note: The script creates and checks out the new branch and initializes the spec file before writing.
