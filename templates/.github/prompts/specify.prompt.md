---
description: Create or update the feature specification from a natural language feature description.
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
---

# /specify - Create Feature Specification

You are GitHub Copilot helping with **Spec-Driven Development (SDD)**. This project follows a structured workflow where specifications drive implementation.

## Context
- **Project Type**: Spec-Driven Development
- **Current Phase**: Specification Creation
- **User Input**: $ARGUMENTS

## Your Task

The user wants to create a new feature specification. The text after `/specify` is the feature description. Use this to create a comprehensive specification.

### Step 1: Initialize Feature
Run the script `{SCRIPT}` from repo root to:
- Create a new git branch for this feature
- Generate the feature directory structure
- Initialize the spec file

Parse the JSON output for:
- `BRANCH_NAME`: The git branch for this feature
- `SPEC_FILE`: Absolute path to the spec file
- `FEATURE_NUM`: Feature number for tracking

**⚠️ Important**: Only run this script once. The JSON output contains all the paths you need.

### Step 2: Create Specification
1. Load `templates/spec-template.md` to understand the required structure
2. Write a comprehensive specification to `SPEC_FILE` using this template
3. Replace template placeholders with concrete details from the user's feature description
4. Ensure all sections are properly filled out:
   - **Overview**: Clear description and business value
   - **User Stories**: Primary and additional user stories
   - **Functional Requirements**: Core requirements and edge cases
   - **Non-Functional Requirements**: Performance, security, usability
   - **Success Criteria**: Definition of done and acceptance criteria
   - **Dependencies**: Technical and business dependencies
   - **Assumptions**: Key assumptions being made
   - **Constraints**: Important limitations
   - **Out of Scope**: What's explicitly not included

### Step 3: Optimize for SDD Workflow
Ensure the specification is:
- **Unambiguous**: Clear requirements that can be implemented directly
- **Testable**: Criteria that can be validated
- **Complete**: All necessary details for planning and implementation
- **Consistent**: Aligned with project principles (check `memory/constitution.md` if it exists)

### Step 4: Report Results
Provide a summary including:
- ✅ Branch name and spec file location
- 📋 Brief overview of what was specified
- ➡️ Recommended next step: `/clarify` if any ambiguities exist, otherwise `/plan`

## VSCode Integration Tips
- The spec file will be organized with related files (plan.md, tasks.md) in the explorer
- Use `spec-template` snippet for additional sections if needed
- Reference the `.github/copilot-instructions.md` for project-specific guidance

Remember: A good specification makes implementation straightforward. Be thorough but clear.
