# Enhanced GitHub Copilot Context for Spec-Driven Development

## Project Context

This file provides enhanced context for GitHub Copilot Chat to understand the Spec-Driven Development (SDD) methodology and project structure.

### Project Type & Methodology
- **Framework**: Spec-Driven Development (SDD)
- **Philosophy**: Specifications are executable and drive implementation
- **Approach**: Systematic, phase-based development with clear documentation

### File Relationships & Dependencies
```
constitution.md ──> spec.md ──> plan.md ──> tasks.md ──> implementation
      ↑               ↑           ↑           ↑
   principles     requirements  architecture  execution
```

### Key Directories & Artifacts
| Location | Purpose |
|----------|---------|
| `memory/constitution.md` | Non-negotiable project principles that govern every decision |
| `.specify/specs/<feature>/spec.md` | Feature requirements and acceptance criteria |
| `.specify/specs/<feature>/plan.md` | Technical architecture and sequencing extracted from the spec |
| `.specify/specs/<feature>/tasks.md` | Ordered implementation tasks with dependencies |
| `.specify/specs/<feature>/data-model.md` | Entities, relationships, and schema constraints |
| `.specify/specs/<feature>/contracts/` | API or integration contracts referenced during implementation |

### Context Hierarchy for Copilot Suggestions
1. **Constitutional Level**: Project principles and standards (`memory/constitution.md`)
2. **Specification Level**: Feature requirements and acceptance criteria (`spec.md`)
3. **Planning Level**: Technical architecture and implementation approach (`plan.md`)
4. **Task Level**: Granular implementation tasks and dependencies (`tasks.md`)
5. **Implementation Level**: Actual code, tests, and documentation

### Enhanced Chat Patterns

#### Context-Rich Specification Requests
```
@workspace Working on user authentication feature.
Context files: memory/constitution.md (security principles), .specify/specs/001-user-auth/spec.md
Requirements: Secure login, password reset, 2FA support
Help me: Complete the specification following our SDD template structure
Consider: GDPR compliance from constitution, existing user model patterns
```

#### Architecture-Aware Planning Requests
```
@workspace Planning microservices architecture for e-commerce.
Context files: .specify/specs/00X-feature/spec.md (requirements), memory/constitution.md (principles)
Tech stack preference: Node.js, PostgreSQL, Redis, Docker
Help me: Generate technical implementation plan with data model and API contracts
Consider: Scalability requirements from spec, performance standards from constitution
```

#### Implementation with Full Context
```
@workspace Implementing UserService from task T014.
Context files: .specify/specs/001-user-auth/plan.md (architecture), .specify/specs/001-user-auth/data-model.md (User entity), .specify/specs/001-user-auth/tasks.md (current task)
Current task: Create UserService with CRUD operations and validation
Help me: Generate the service class following our established patterns
Consider: Error handling patterns from plan, validation rules from data model
```

### Cross-Reference Validation Patterns
- Validate implementations against specification requirements
- Ensure architectural decisions align with project principles
- Check task completion against acceptance criteria
- Verify code patterns match established conventions
- Confirm documentation stays current with implementation

### Slash Command Quick Reference
| Command | Purpose |
|---------|---------|
| `/specify` | Create a new feature specification and branch using project templates |
| `/clarify` | Resolve ambiguous requirements and document clarifications inside the spec |
| `/plan` | Produce architecture, data models, and implementation sequencing |
| `/tasks` | Generate granular execution tasks with dependencies |
| `/implement` | Drive the build process using the generated tasks and context |
| `/analyze` | Cross-check spec, plan, and tasks for inconsistencies before coding |

This enhanced context enables GitHub Copilot to provide more intelligent, project-aware assistance throughout the Spec-Driven Development lifecycle.
