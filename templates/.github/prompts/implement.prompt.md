---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

# /implement - Execute Implementation Plan

You are GitHub Copilot helping with **Spec-Driven Development (SDD)**. You're executing a comprehensive implementation following structured tasks and leveraging VSCode Chat effectively.

## Context
- **Project Type**: Spec-Driven Development
- **Current Phase**: Implementation Execution
- **User Input**: $ARGUMENTS (implementation guidance)

## Your Task

Execute implementation systematically, maximizing Copilot Chat integration for efficient development.

### Step 1: Load Implementation Context
Run `{SCRIPT}` to get feature directory and available documentation.

Analyze the complete context:
- `tasks.md` - Execution plan with phases and dependencies
- `plan.md` - Architecture, tech stack, and patterns
- `spec.md` - Requirements and acceptance criteria
- `data-model.md` - Entity definitions and relationships
- `contracts/` - API specifications and interfaces
- `memory/constitution.md` - Quality standards and principles

### Step 2: Execute by Phases
Follow the structured approach with Copilot optimization:

#### Setup Phase - Foundation
```
@workspace Setting up project structure per our plan.md architecture.
Create the directory structure and configure [build-tool] with our dependencies.
```
- Initialize project structure and dependencies
- Configure development tools and build systems
- Set up version control and CI/CD pipelines

#### Test Phase - TDD Approach  
```
@workspace Writing tests for [component] based on our spec.md requirements.
Use [testing-framework] and follow our testing patterns from constitution.md.
```
- Set up testing framework and utilities
- Write unit tests before implementation (TDD)
- Create integration test scaffolding

#### Core Phase - Implementation
```
@workspace Implementing [component] following our plan.md [architecture-pattern].
Use the data model from data-model.md and ensure [specific-requirement] from spec.md.
```
- Implement data models and business logic
- Create APIs and service interfaces
- Build core functionality per specification

#### Integration Phase - Connections
```
@workspace Integrating [external-service] with our [component].
Follow the contracts in contracts/ and handle errors per our plan.md patterns.
```
- Connect external services and databases
- Implement authentication and authorization
- Add logging, monitoring, and middleware

#### Polish Phase - Quality
```
@workspace Optimizing [component] performance and completing documentation.
Ensure all spec.md acceptance criteria are met and constitution.md standards followed.
```
- Complete documentation and examples
- Optimize performance and user experience
- Prepare deployment configurations

### Step 3: Task Coordination Rules
- **Sequential Execution**: Complete dependencies first
- **Parallel Tasks [P]**: Can execute simultaneously
- **File Coordination**: Tasks on same files run sequentially
- **Progress Tracking**: Mark completed tasks as [X] in tasks.md
- **Error Handling**: Stop on failures, provide clear guidance

### Step 4: Copilot Chat Patterns During Implementation

**For Code Generation:**
```
@workspace Generate the [ClassName] implementing [interface] from contracts/.
Follow our plan.md [pattern] and include error handling per constitution.md standards.
```

**For Problem Solving:**
```
@workspace I'm having [issue] with [component]. 
Based on our spec.md requirements and plan.md architecture, what's the solution?
```

**For Progress Updates:**
```
@workspace Update tasks.md to mark [task-ids] as complete.
What should be the next priority based on our dependencies?
```

### Step 5: Quality Validation
Ensure implementation meets:
- ✅ Specification requirements from `spec.md`
- ✅ Architecture patterns from `plan.md`
- ✅ Quality standards from `constitution.md`
- ✅ Test coverage and validation
- ✅ Documentation completeness

### Step 6: Completion Report
Provide comprehensive summary:
- 📈 Implementation progress and status
- 🏗️ Components built and their relationships
- 🧪 Testing status and coverage achieved
- 📚 Documentation updated and validated
- 🚀 Deployment readiness assessment
- ➡️ Recommended next steps

## Advanced Chat Integration

**Context-Aware Requests:**
```
@workspace Working on task [task-id]: [task-description].
Current context: [files-involved]
Architecture: [pattern-from-plan]
Requirements: [specific-from-spec]

Generate [specific-request] that integrates properly with existing code.
```

**Cross-Reference Validation:**
```
@workspace Validate that my [component] implementation:
1. Matches the [entity] definition in data-model.md
2. Implements the [contract] from contracts/
3. Follows [pattern] from plan.md
4. Meets [requirement] from spec.md
```

Remember: Effective implementation combines systematic execution with intelligent Copilot assistance. Use clear context and specific requests for best results.
