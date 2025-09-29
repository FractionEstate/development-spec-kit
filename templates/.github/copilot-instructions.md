# GitHub Copilot Instructions for Spec-Driven Development

## Project Context

This is a **Spec-Driven Development (SDD)** project where specifications are executable and drive implementation. The project follows a structured workflow that prioritizes clear requirements and systematic development.

## Development Workflow

### Phase Overview
1. **Constitution** (`/constitution`) - Define project principles and standards
2. **Specify** (`/specify`) - Create detailed feature specifications
3. **Clarify** (`/clarify`) - Resolve ambiguities and edge cases
4. **Plan** (`/plan`) - Generate technical implementation plans
5. **Tasks** (`/tasks`) - Break down into actionable tasks
6. **Implement** (`/implement`) - Execute the implementation
7. **Analyze** (`/analyze`) - Validate consistency and completeness

### Key Files Structure
```
project-root/
└── .specify/
    ├── memory/
    │   └── constitution.md          # Project principles
    ├── specs/
    │   └── feature-*/
    │       ├── spec.md             # Feature specification
    │       ├── plan.md             # Implementation plan
    │       ├── tasks.md            # Task breakdown
    │       ├── data-model.md       # Data models (if applicable)
    │       ├── contracts/          # API contracts (if applicable)
    │       ├── quickstart.md       # Integration guide (if applicable)
│       └── research.md         # Technical research (if applicable)
└── .github/
    └── prompts/                # Copilot command prompts
```

## Chat Interaction Guidelines

### When Providing Assistance

1. **Always consider the full context:**
   - Check `memory/constitution.md` for project principles
   - Review the current feature's `spec.md` for requirements
   - Examine `plan.md` for technical decisions
   - Reference `tasks.md` for implementation progress

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
   Current files: spec.md, plan.md, tasks.md

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
Current spec.md has [current state].
Please help me [specific need] while following our constitution.md principles.
```

**For Implementation:**
```
@workspace I need to implement [specific task] from tasks.md.
The plan.md specifies [technical approach].
Please generate code that [specific requirement].
```

**For Debugging:**
```
@workspace I'm having an issue with [component].
Based on our spec.md requirements and plan.md architecture,
what could be causing [problem description]?
```

## Prompt Quick Reference

| Command | Purpose | Copilot Tips |
|---------|---------|--------------|
| `/specify` | Generate or update feature specification | Provide the raw user intent; review the output for `[NEEDS CLARIFICATION: ...]` markers and resolve via `/clarify` before planning. |
| `/clarify` | Resolve ambiguities in the specification | Answer each clarification in plain language so subsequent commands can remove blockers. |
| `/plan` | Produce technical architecture and supporting artifacts | Supply tech stack preferences in the command arguments and capture any residual risks in the summary for future phases. |
| `/tasks` | Derive actionable implementation tasks | Look for `[P]` tasks to identify safe parallelization; use the provided @workspace examples to kick off coding sessions. |
| `/implement` | Execute the plan with Copilot-driven coding | Update `tasks.md` as you work; reuse the summary’s @workspace prompts to maintain momentum. |
| `/analyze` | Cross-check artifacts for consistency gaps | Run after `/tasks` or implementation cycles to spot misalignments before shipping. |

Keep this table in view while working; it captures when to run each command and how to get the most from GitHub Copilot Chat at every stage.

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
- `spec-template` - Complete feature specification template
- `copilot-context` - Structured context for Copilot Chat
- `sdd-chat` - Enhanced chat request template

### File Organization
The project uses file nesting in VS Code:
- `spec.md` groups with related files (`plan.md`, `tasks.md`, etc.)
- `constitution.md` groups with memory files
- Enhanced search excludes build artifacts and dependencies

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

Remember: GitHub Copilot Chat works best when provided with clear context about the current development phase, relevant files, and specific questions. Always reference the SDD workflow and project structure for optimal assistance.

## 🔗 Additional Resources

For enhanced Copilot integration:
- **[Enhanced Context Guide](./copilot-context.md)** - Advanced context patterns and chat optimization
- **[Reference Links](./copilot-references.md)** - Comprehensive documentation and resource links
- **[VSCode Snippets](../.vscode/spec-driven-dev.code-snippets)** - Quick templates for structured Copilot conversations
- **[Project Documentation](../README-copilot.md)** - Copilot-specific usage guide for this project

Use these resources to maximize the effectiveness of your GitHub Copilot interactions in Spec-Driven Development projects.
