---
description: Generate actionable task breakdown from implementation plan for systematic development execution.
---

<!-- prompt-scripts
sh: scripts/bash/check-prerequisites.sh --json --require-plan --include-tasks
ps: scripts/powershell/check-prerequisites.ps1 -Json -RequirePlan -IncludeTasks
-->

# /tasks - Generate Task Breakdown

You are GitHub Copilot helping with **Spec-Driven Development (SDD)**. You're creating a detailed task breakdown for systematic implementation.

## Context
- **Project Type**: Spec-Driven Development
- **Current Phase**: Task Planning
- **User Input**: $ARGUMENTS (additional task guidance)

## Your Task

Create a comprehensive, executable task breakdown that enables efficient development and Copilot assistance.

### Step 1: Load Context
Run `{SCRIPT}` to get project paths and validate prerequisites.

Load implementation context:
- `spec.md` - Feature requirements and acceptance criteria
- `plan.md` - Technical architecture and decisions
- `data-model.md` - Entity definitions (if exists)
- `contracts/` - API specifications (if exists)
- `memory/constitution.md` - Project standards (if exists)

### Step 2: Generate Structured Tasks
Use `templates/tasks-template.md` as the blueprint. Produce phased sections (`Phase 3.1` through `Phase 3.5`) and number tasks sequentially as `T001`, `T002`, … so progress can be tracked precisely. Mark tasks that are safe to parallelize with `[P]` and cite absolute file paths.

**Phase 3.1 – Setup**
- Project skeleton, tooling, and dependency installation
- Environment and configuration scaffolding

**Phase 3.2 – Tests First (TDD)**
- Contract and integration tests that must fail before implementation
- Unit test harnesses and fixtures

**Phase 3.3 – Core Implementation**
- Data models, services, endpoints, and business logic

**Phase 3.4 – Integration**
- External service wiring, middleware, observability hooks

**Phase 3.5 – Polish**
- Documentation, performance, cleanup, manual validation

### Step 3: Optimize for Copilot Workflow
Each task should include:
- **Clear scope** - Specific files, components, and patterns to touch (absolute paths when possible)
- **Dependencies** - Prerequisites and ordering; reference task IDs explicitly
- **Acceptance criteria** - How to validate completion and required tests/documentation updates
- **Copilot hints** - Concrete context for better code generation (mention relevant plan sections/contracts)
- **Completion markers** - Use checkbox lists so the implementation agent can mark `[x]` as they progress

### Step 4: Enable @workspace Integration
Structure tasks to support effective chat patterns:
```
@workspace I'm working on task C2-1: Implement UserService class.
Based on our data-model.md User entity and plan.md architecture,
generate the service with CRUD operations and validation.
```
- Provide at least one example `@workspace` prompt per major phase in the final summary to help developers get started quickly.

## Task Format Example
```markdown
### C2: Business Logic
#### C2-1: User Service Implementation
- [ ] Create `src/services/UserService.js` with CRUD operations
- [ ] Implement validation using data-model.md User schema
- [ ] Add error handling per plan.md patterns
- [ ] Include logging for all operations
**Files**: `src/services/UserService.js`, `src/models/User.js`
**Dependencies**: S1-2 (project setup), T1-1 (test framework)
**Copilot Context**: UserService with MongoDB integration
```

### Step 5: Report Results
Provide a Markdown summary that includes:
- ✅ **Tasks file status** – Confirmation that phased sections mirror the template and the path to `tasks.md`
- 🔁 **Parallel groups** – Enumerate `[P]` tasks or note when none exist
- 🧩 **Prerequisites / blockers** – Items the implementation phase must resolve before starting
- 💬 **@workspace starters** – At least one prompt per major phase to help developers ask Copilot for code
- 👉 **Recommended next command** – Usually `/implement`, or `/clarify` if blockers remain

Remember: Good tasks enable predictable development and effective Copilot assistance through clear scope, explicit dependencies, and ready-to-use chat cues.
