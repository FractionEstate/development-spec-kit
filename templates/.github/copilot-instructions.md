# GitHub Copilot Instructions for Spec-Driven Development

This document primes GitHub Copilot for the Spec-Driven Development (SDD) workflow. Pair it with `templates/README-copilot.md` before each session so Copilot always operates with the same premium-quality context the team sees.

## Quick Orientation

| Focus | Canonical Location | Use It For |
|-------|--------------------|------------|
| Project Constitution | `.specify/memory/constitution.md` | Principles, test mandates, and review guardrails that apply to every feature. |
| Active Feature Artifacts | `.specify/specs/<feature>/` | Authoritative `spec.md`, `plan.md`, `tasks.md`, plus optional data model, contracts, research, quickstart. |
| Copilot System Prompts | `.github/copilot-instructions.md`, `.github/copilot-context.md` | Baseline guidance and ready-to-send prompts that keep Copilot grounded. |
| Reference Library | `.github/copilot-references.md` | Curated documentation, checklists, and supporting links. |
| VS Code Workflow | `.vscode/` | Settings, tasks, and snippets tuned for the SDD cadence. |

## Workspace Layout

```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md                 # Governance and standards
│   └── specs/
│       └── <feature-slug>/
│           ├── spec.md                     # Feature requirements & acceptance criteria
│           ├── plan.md                     # Architecture, sequencing, risk notes
│           ├── tasks.md                    # Ordered, testable work items
│           ├── data-model.md               # Entities and schema constraints (optional)
│           ├── contracts/                  # API/integration contracts (optional)
│           ├── quickstart.md               # Integration smoke tests (optional)
│           └── research.md                 # Supporting analysis (optional)
├── .github/
│   ├── copilot-instructions.md             # This file
│   ├── copilot-context.md                  # Ready-to-send context bundles
│   ├── copilot-references.md               # Extended references & links
│   └── prompts/                            # Slash-command prompt set
└── .vscode/
    ├── settings.json                       # Copilot-optimized configuration
    ├── tasks.json                          # SDD slash-command wiring
    └── spec-driven-dev.code-snippets       # Context-aware template snippets
```

## Development Workflow

### Phase Overview
1. **Constitution** (`/constitution`) – Define or refine project principles and standards.
2. **Specify** (`/specify`) – Capture requirements and acceptance criteria in `spec.md`.
3. **Clarify** (`/clarify`) – Resolve outstanding questions before planning begins.
4. **Plan** (`/plan`) – Produce architecture, sequencing, and risk notes in `plan.md`.
5. **Tasks** (`/tasks`) – Generate ordered, testable work items in `tasks.md`.
6. **Implement** (`/implement`) – Execute coding work while updating tasks for progress and blockers.
7. **Analyze** (`/analyze`) – Cross-audit artifacts to catch drift before review or release.

Every command writes to `.specify/specs/<feature>/`, maintaining a single source of truth for the entire feature.

> Need the full slash-command loop? See the “Feature Bootstrap Walkthrough” table in `README-copilot.md` for an end-to-end checklist.

## Chat Interaction Guidelines

### When Providing Assistance

1. **Always consider the full context:**
   - Check `memory/constitution.md` for project principles
   - Review the current feature's `.specify/specs/<feature>/spec.md` for requirements
   - Examine `.specify/specs/<feature>/plan.md` for technical decisions
   - Reference `.specify/specs/<feature>/tasks.md` for implementation progress

2. **Maintain SDD principles:**
   - Specifications should be clear and unambiguous
   - Implementation should match the specification exactly
   - Technical decisions should be documented in the plan
   - Tasks should be granular and testable

3. **Provide structured responses:**
   - Reference specific files and sections
   - Explain how suggestions align with the spec
   - Consider impact on other project components
   - Suggest updates to documentation when needed

### Code Generation Guidelines

#### For Specifications (`.md` files)
- Use clear, unambiguous language
- Include concrete acceptance criteria
- Specify edge cases and error conditions
- Reference project constitution requirements

#### For Implementation Code
- Follow the technical stack defined in `plan.md`
- Implement only features specified in `spec.md`
- Include appropriate error handling
- Add tests as defined in `tasks.md`
- Follow code style from constitution

#### For Documentation
- Keep consistency with existing docs
- Update related files when making changes
- Include examples and usage scenarios
- Reference specification sections

### VSCode Chat Optimization

#### Best Practices for @workspace conversations:
1. **Use context markers:**
   ```
   @workspace Working on [feature-name] in the [phase] phase
   Current files: .specify/specs/<feature>/spec.md, .specify/specs/<feature>/plan.md, .specify/specs/<feature>/tasks.md

   Question: [Your specific question]
   ```

2. **Request structured outputs:**
   - "Generate code that follows the plan.md architecture"
   - "Update tasks.md to mark completed items"
   - "Suggest spec.md improvements for better clarity"

3. **Leverage workspace awareness:**
   - Reference specific file sections
   - Ask for cross-file consistency checks
   - Request impact analysis of proposed changes

#### Common Chat Patterns:

**For Specification Writing:**
```
@workspace I'm working on the [feature] specification.
Current file: .specify/specs/<feature>/spec.md shows [current state].
Please help me [specific need] while following our constitution.md principles.
```

**For Implementation:**
```
@workspace I need to implement [specific task] from .specify/specs/<feature>/tasks.md.
.specify/specs/<feature>/plan.md specifies [technical approach].
Please generate code that [specific requirement].
```

**For Debugging:**
```
@workspace I'm having an issue with [component].
Based on .specify/specs/<feature>/spec.md requirements and .specify/specs/<feature>/plan.md architecture,
what could be causing [problem description]?
```

## Prompt Quick Reference

| Command | Purpose | Copilot Prompt Tips |
|---------|---------|---------------------|
| `/specify` | Generate or evolve a feature specification | Feed raw intent plus blockers. Resolve `[NEEDS CLARIFICATION]` items via `/clarify` before planning. |
| `/clarify` | Remove ambiguities discovered in specs or reviews | Answer each clarification inline so downstream commands stay unblocked. |
| `/plan` | Produce architecture, sequencing, and risk notes | Provide stack preferences and capture trade-offs in the summary for future phases. |
| `/tasks` | Derive ordered, testable work items | Highlight parallel `[P]` tasks and dependencies for smoother implementation. |
| `/implement` | Execute the plan with Copilot-driven coding | Reference specific `tasks.md` entries and update progress immediately after code changes. |
| `/analyze` | Cross-audit artifacts for drift | Run before handoff or release to surface spec/plan/tasks mismatches. |
| `/constitution` | Establish or refine project principles | Use during inception or governance refreshes; cite sections when making trade-offs. |

Keep this table visible; it anchors when to run each command and how to prime Copilot for precise, phase-aware support.

## Integration Features

### Available VSCode Tasks
Use Ctrl+Shift+P → "Tasks: Run Task" to access:
- **Specify: Create Feature** - Launch `/specify` command
- **Plan: Generate Implementation Plan** - Launch `/plan` command
- **Tasks: Generate Task Breakdown** - Launch `/tasks` command
- **Implement: Execute Implementation** - Launch `/implement` command
- **Constitution: Set Project Principles** - Launch `/constitution` command
- **Clarify: Resolve Ambiguities** - Launch `/clarify` command
- **Analyze: Cross-Artifact Analysis** - Launch `/analyze` command

### Code Snippets
Type these prefixes in markdown files for quick templates:
| `spec-template` - Complete feature specification template
| `copilot-context` - Structured context for Copilot Chat
| `sdd-chat` - Enhanced chat request template
| `feature-bootstrap` - Drop-in walkthrough table for end-to-end command flow

### File Organization
The project uses file nesting in VS Code:
- `spec.md` groups with related files (`plan.md`, `tasks.md`, etc.)
- `constitution.md` groups with memory files
- Enhanced search excludes build artifacts and dependencies

## Agent tools & capabilities

Use these capabilities explicitly in prompts to guide high-quality actions:

- File edits & creation: "Edit `templates/README-copilot.md` to add an Agent Tools section"
- Workspace search: "Search for all mentions of `feature-bootstrap` and list files"
- Targeted file reads: "Read `copilot-references.md` and summarize the SDD table"
- Terminal commands: "Run `git status -sb` and report modified files"
- VS Code tasks: "Run the 'Tasks: Generate Task Breakdown' task"
- Snippets: "Insert the `feature-bootstrap` snippet here"
- Notebooks (if present): "Run the first code cell in `<notebook>.ipynb`"
- Browser preview (optional): "Open our docs homepage to check layout"
- Session TODO tracking: "Start a TODO list with items A/B/C and mark A in-progress"

Provide exact file paths, expected outcomes, and any guardrails (e.g., "change only the table, leave intro untouched").

## Quality Standards

### Code Quality
- Follow the testing requirements from `constitution.md`
- Implement comprehensive error handling
- Include appropriate logging and monitoring
- Maintain clean, readable code structure

### Documentation Quality
- Keep specifications current with implementation
- Update plans when making architectural changes
- Maintain task progress in `tasks.md`
- Document decisions in appropriate files

### Consistency Standards
- Ensure spec-to-implementation alignment
- Maintain consistent terminology across files
- Follow established patterns and conventions
- Validate cross-file references and dependencies

## Troubleshooting

### Common Issues and Solutions

**Specification Ambiguity:**
- Run `/clarify` to resolve unclear requirements
- Add concrete examples and edge cases
- Define acceptance criteria more specifically

**Implementation Drift:**
- Compare current code against `spec.md` requirements
- Review `plan.md` for architectural compliance
- Check `tasks.md` for missed or incomplete items

**Integration Problems:**
- Verify `quickstart.md` integration scenarios
- Check `data-model.md` for entity relationships
- Review `contracts/` for API specifications

**Performance Issues:**
- Reference performance requirements from `spec.md`
- Check implementation against `plan.md` architecture
- Consider constitution performance standards

Remember: Copilot Chat performs best when your prompt names the current phase, points to the exact `.specify/specs/<feature>/` files involved, and cites relevant constitution guardrails. Keep the SDD workflow front and center to maintain premium-quality responses.

## Resource Hub

- **Primary Instructions** – `.github/copilot-instructions.md`
- **Enhanced Context Guide** – `.github/copilot-context.md`
- **Reference Library** – `.github/copilot-references.md`
- **VS Code Snippets** – `.vscode/spec-driven-dev.code-snippets`
- **Copilot README Playbook** – `README-copilot.md`

Consult these assets in tandem to keep Copilot briefing, prompts, and VS Code automation perfectly aligned.
