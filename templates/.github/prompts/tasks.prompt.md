---
description: Generate actionable task breakdown from implementation plan for systematic development execution.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-plan --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequirePlan -IncludeTasks
---

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
Create tasks organized by phases:

**Setup Phase (S1-S2)**
- Project structure initialization
- Dependencies and tooling setup
- Development environment configuration

**Test Phase (T1-T2)**  
- Testing framework setup
- Test utilities and mocks
- Core component tests (following TDD)

**Core Phase (C1-C3)**
- Data layer implementation
- Business logic development
- API/interface creation

**Integration Phase (I1-I2)**
- External service integration
- Database connections
- Authentication and middleware

**Polish Phase (P1-P3)**
- Documentation completion
- Performance optimization
- Deployment preparation

### Step 3: Optimize for Copilot Workflow
Each task should include:
- **Clear scope** - Specific files and components
- **Dependencies** - Prerequisites and ordering
- **Acceptance criteria** - How to validate completion
- **Copilot hints** - Context for better code generation

### Step 4: Enable @workspace Integration
Structure tasks to support effective chat patterns:
```
@workspace I'm working on task C2-1: Implement UserService class.
Based on our data-model.md User entity and plan.md architecture,
generate the service with CRUD operations and validation.
```

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

Remember: Good tasks enable predictable development and effective Copilot assistance through clear scope and context.
