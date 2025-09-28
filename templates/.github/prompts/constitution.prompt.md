---
description: Define project principles and governance rules that guide all development decisions.
---

# /constitution - Establish Project Principles

You are GitHub Copilot helping with **Spec-Driven Development (SDD)**. This project follows a structured workflow where project principles guide all development decisions.

## Context
- **Project Type**: Spec-Driven Development
- **Current Phase**: Constitution Creation
- **User Input**: $ARGUMENTS

## Your Task

The user wants to establish or update the project constitution that defines core principles, governance rules, and development standards.

### Step 1: Load Constitution Template
1. Load the existing constitution template at `/memory/constitution.md`
2. Identify all placeholder tokens in square brackets (e.g., `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`)
3. Note any existing content if this is an update to an established constitution

### Step 2: Gather Information
Collect values for placeholders from:
- User input provided in the conversation
- Existing repository context (README, docs, prior versions)
- Interactive questions if critical information is missing

Key information needed:
- **Project name and description**
- **Core principles** (usually 3-5 key principles)
- **Governance details** (decision-making, amendment process)
- **Version information** (for updates: proper semantic versioning)

### Step 3: Draft Constitution Content
1. Replace all placeholder tokens with concrete values
2. Ensure each principle has:
   - Clear, memorable name
   - Specific, actionable description
   - Explicit rationale for why it matters
3. Include governance section with:
   - Amendment procedures
   - Version control policy
   - Compliance expectations

### Step 4: Validate and Sync
Before finalizing:
1. Check consistency with existing templates:
   - `/templates/plan-template.md` for alignment
   - `/templates/spec-template.md` for required sections
   - `/templates/tasks-template.md` for task categories
2. Update any templates that reference outdated principles
3. Note any documentation that needs updates

### Step 5: Version Management
For constitution updates:
- **MAJOR version**: Breaking changes, removed principles
- **MINOR version**: New principles or expanded guidance
- **PATCH version**: Clarifications, wording improvements

### Step 6: Write and Report
1. Write the completed constitution to `/memory/constitution.md`
2. Create a sync impact report as HTML comment at the top
3. List any templates or docs that need manual updates

### Step 7: Provide Copilot-Ready Summary
End your response with a labeled Markdown summary containing:
- ✅ **Constitution version** – New version number and bump rationale
- 📋 **Key principles** – List of established principles with brief descriptions
- 🔄 **Impact assessment** – Files that may need updates due to changes
- ⚠️ **Manual follow-ups** – Any templates or docs requiring manual review
- 🧭 **Next @workspace starter** – Ready-to-copy prompt for reviewing affected files
- ➡️ **Recommended next command** – Usually `/specify` to begin feature work, or file reviews if updates needed

Example starter:
```
@workspace Review the files flagged in the constitution sync report and update any references to the new principles.
```

## VSCode Integration Tips
- Constitution file will be available in `.specify/memory/constitution.md`
- Use constitution principles to guide specification and planning decisions
- Reference principles in code comments and documentation

Remember: A strong constitution provides clear decision-making guidance and ensures consistent project values across all development work.
