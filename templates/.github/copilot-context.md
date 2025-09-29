# Enhanced GitHub Copilot Context for Spec-Driven Development

## Project Context

This brief keeps GitHub Copilot grounded in the Spec-Driven Development (SDD) workflow. Pair it with the refreshed `README-copilot.md` to deliver precise, phase-aware assistance every time.

### Quick Orientation

| Focus | Canonical Location | Use It For |
|-------|--------------------|------------|
| Project principles | `.specify/memory/constitution.md` | Governance, testing standards, and decision guardrails |
| Active feature assets | `.specify/specs/<feature>/` | `spec.md`, `plan.md`, `tasks.md`, plus optional data models, contracts, research |
| Conversation blueprints | `.github/copilot-instructions.md` & `.github/copilot-context.md` | Baseline guidance and ready-to-send prompts |
| Deep reference library | `.github/copilot-references.md` | Extended documentation, checklists, and supporting links |
| VS Code workflow | `.vscode/` | Settings, tasks, and snippets optimized for SDD |

### Workspace Layout

```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   └── specs/
│       └── <feature-slug>/
│           ├── spec.md
│           ├── plan.md
│           ├── tasks.md
│           ├── data-model.md
│           ├── contracts/
│           ├── quickstart.md
│           └── research.md
├── .github/
│   ├── copilot-instructions.md
│   ├── copilot-context.md
│   ├── copilot-references.md
│   └── prompts/
└── .vscode/
    ├── settings.json
    ├── tasks.json
    └── spec-driven-dev.code-snippets
```

### File Relationships & Dependencies
```
constitution.md  →  spec.md  →  plan.md  →  tasks.md  →  implementation
        ↑             ↑           ↑           ↑
   principles     requirements  architecture  execution
```

### Context Hierarchy for Copilot Suggestions
1. **Constitutional Level** – `memory/constitution.md`
2. **Specification Level** – `.specify/specs/<feature>/spec.md`
3. **Planning Level** – `.specify/specs/<feature>/plan.md`
4. **Task Level** – `.specify/specs/<feature>/tasks.md`
5. **Implementation Level** – Source code, tests, and integration docs

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
| Command | Purpose | Copilot Prompt Tips |
|---------|---------|---------------------|
| `/specify` | Generate or evolve a feature specification | Feed raw intent plus blockers; resolve `[NEEDS CLARIFICATION]` markers before planning. |
| `/clarify` | Eliminate ambiguities flagged by specs or reviewers | Answer each clarification inline so downstream commands stay unblocked. |
| `/plan` | Produce architecture, sequencing, and risk notes | Provide stack preferences; capture trade-offs and open questions in the summary. |
| `/tasks` | Derive ordered, testable work items | Highlight parallelizable `[P]` tasks and dependencies for smooth implementation. |
| `/implement` | Execute against the approved plan | Reference specific `tasks.md` entries and confirm updates after each coding block. |
| `/analyze` | Cross-audit artifacts for drift | Run before handoff or release to surface gaps between spec, plan, tasks, and code. |
| `/constitution` | Establish or revise project principles | Use during inception or governance refreshes; cite sections when making trade-offs. |

### Resource Hub
- **Primary Instructions** – `.github/copilot-instructions.md`
- **Conversation Playbook** – `.github/copilot-context.md`
- **Reference Library** – `.github/copilot-references.md`
- **Workflow Snippets** – `.vscode/spec-driven-dev.code-snippets`
- **Copilot README** – `templates/README-copilot.md`
- **Feature Bootstrap Walkthrough** – `templates/README-copilot.md#feature-bootstrap-walkthrough`
- **Snippet: Feature Bootstrap** – `templates/.vscode/spec-driven-dev.code-snippets` (`feature-bootstrap`)

### Agent tools (quick reference)
- Edits & creates files on request
- Searches and reads files by path or pattern
- Runs one-line terminal commands and summarizes
- Launches VS Code tasks wired to slash commands
- Inserts snippets like `feature-bootstrap`
- Maintains a session TODO when asked
- Optional: notebooks and simple browser preview

See `templates/README-copilot.md#agent-tools--capabilities` for details and prompt examples.

Use this brief as the companion to the `README-copilot.md` playbook. Load the relevant `.specify/specs/<feature>/` files before each session, cite constitution guardrails, and Copilot will consistently deliver premium guidance across the SDD lifecycle.
