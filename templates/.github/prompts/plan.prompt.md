---
description: Create technical architecture and implementation roadmap from your feature specification.
---

<!-- prompt-scripts
sh: scripts/bash/setup-plan.sh --json
ps: scripts/powershell/setup-plan.ps1 -Json
-->

# /plan - Generate Implementation Plan

You are GitHub Copilot helping with **Spec-Driven Development (SDD)**. You're creating a technical implementation plan based on an existing specification.

## Context
- **Project Type**: Spec-Driven Development
- **Current Phase**: Implementation Planning
- **User Input**: $ARGUMENTS (technical implementation details)

## Your Task

Transform the feature specification into a concrete technical implementation plan with VSCode Chat optimization.

### Step 1: Validate Prerequisites
Run `{SCRIPT}` from repo root and parse the JSON output for paths and validation.

**Before continuing**: Verify the specification has proper clarifications. If critical ambiguities remain, recommend `/clarify` first.

### Step 2: Create Comprehensive Plan
Generate technical implementation plan including:
- **Technical Stack**: Languages, frameworks, databases, tools (pull in user-provided preferences from arguments)
- **Architecture**: System design, component relationships, data flow (reference constitution constraints)
- **Project Structure**: File organization, module breakdown with absolute paths
- **Development Guidelines**: Code style, testing approach, documentation standards with explicit success checks
- **Risk & Mitigation Notes**: Highlight tricky areas the implementation agent should watch for

### Step 3: Generate Supporting Artifacts
Based on the plan template execution:
- `research.md` - Technical analysis and decisions
- `data-model.md` - Entity definitions and relationships
- `contracts/` - API specifications and interfaces
- `quickstart.md` - Setup and integration guide
- `tasks.md` - Structured task breakdown

Ensure artifacts cross-link to each other (e.g., reference entity names consistently) so Copilot can navigate context easily.

### Step 4: Optimize for Copilot Chat
Ensure the plan enables effective @workspace conversations by:
- Using specific technology names for better code suggestions
- Defining clear architectural patterns and pointing to file locations to anchor requests
- Establishing consistent naming conventions across plan, data models, and contracts
- Including concrete examples and patterns plus `@workspace` snippets the user can copy
- Calling out prerequisite clarifications or environment setup steps the implementation phase must execute first

## Chat Integration Example
After planning, developers can use:
```
@workspace Based on our plan.md Node.js/Express architecture,
help me implement the UserController with proper error handling
and validation following our established patterns.
```

### Step 5: Report & Next Actions
Summarize your work with a structured Markdown block that includes:
- ✅ **Plan status** – Progress Tracking checklist results (Phase 0/1, Gate checks)
- 📁 **Generated artifacts** – Absolute paths for `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md` status
- 🔍 **Architecture highlights** – 1-2 bullets explaining pivotal decisions and why they align with the constitution
- ❓ **Open questions / risks** – Items that require attention before coding or during `/tasks`
- 💬 **Next @workspace starter** – Ready-to-use prompt to begin `/tasks` or a remediation step
- 👉 **Recommended next command** – Usually `/tasks` when confident, otherwise `/clarify` with the specific blocker

Remember: A good plan makes Copilot suggestions more accurate and implementation more predictable by providing clear entry points for each phase.
