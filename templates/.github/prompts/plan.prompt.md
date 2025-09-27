---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
---

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
- **Technical Stack**: Languages, frameworks, databases, tools
- **Architecture**: System design, component relationships, data flow
- **Project Structure**: File organization, module breakdown
- **Development Guidelines**: Code style, testing approach, documentation standards

### Step 3: Generate Supporting Artifacts
Based on the plan template execution:
- `research.md` - Technical analysis and decisions
- `data-model.md` - Entity definitions and relationships  
- `contracts/` - API specifications and interfaces
- `quickstart.md` - Setup and integration guide
- `tasks.md` - Structured task breakdown

### Step 4: Optimize for Copilot Chat
Ensure the plan enables effective @workspace conversations by:
- Using specific technology names for better code suggestions
- Defining clear architectural patterns
- Establishing consistent naming conventions
- Including concrete examples and patterns

## Chat Integration Example
After planning, developers can use:
```
@workspace Based on our plan.md Node.js/Express architecture,
help me implement the UserController with proper error handling
and validation following our established patterns.
```

Remember: A good plan makes Copilot suggestions more accurate and implementation more predictable.
