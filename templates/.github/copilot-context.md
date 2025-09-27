# Enhanced GitHub Copilot Context & References

## Model Context Protocol (MCP) Integration

This file provides enhanced context for GitHub Copilot Chat to understand the Spec-Driven Development (SDD) methodology and project structure.

### Project Type & Methodology
- **Framework**: Spec-Driven Development (SDD)
- **Philosophy**: Specifications are executable and drive implementation
- **Approach**: Systematic, phase-based development with clear documentation

### Key Reference Links & Resources

#### Spec-Driven Development Resources
- **SDD Methodology**: [Spec-Driven Development Guide](https://github.com/FractionEstate/spec-kit)
- **Best Practices**: [SDD Best Practices Documentation](./README-copilot.md)
- **Workflow Guide**: [Development Phases](./copilot-instructions.md#development-workflow)

#### GitHub Copilot Optimization Resources
- **Copilot Documentation**: https://docs.github.com/en/copilot
- **VSCode Chat Guide**: https://code.visualstudio.com/docs/copilot/copilot-chat
- **Workspace Context**: https://code.visualstudio.com/docs/copilot/workspace-context
- **Chat Participants**: https://code.visualstudio.com/docs/copilot/copilot-extensibility-overview

#### Development Patterns & Templates
- **Specification Templates**: [spec-template.md](../spec-template.md)
- **Implementation Patterns**: [plan-template.md](../plan-template.md)
- **Task Management**: [tasks-template.md](../tasks-template.md)
- **Code Snippets**: [VSCode Snippets](../.vscode/spec-driven-dev.code-snippets)

### Context Protocol Guidelines

#### File Relationships & Dependencies
```
constitution.md ──> spec.md ──> plan.md ──> tasks.md ──> implementation
      ↑               ↑           ↑           ↑
   principles     requirements  architecture  execution
```

#### Context Hierarchy for Copilot Suggestions
1. **Constitutional Level**: Project principles and standards (`memory/constitution.md`)
2. **Specification Level**: Feature requirements and acceptance criteria (`spec.md`)
3. **Planning Level**: Technical architecture and implementation approach (`plan.md`)
4. **Task Level**: Granular implementation tasks and dependencies (`tasks.md`)
5. **Implementation Level**: Actual code, tests, and documentation

#### Semantic Context Markers
Use these markers in conversations to help Copilot understand context:

- `[SDD-PHASE:specify]` - Currently in specification phase
- `[SDD-PHASE:plan]` - Currently in planning phase
- `[SDD-PHASE:implement]` - Currently in implementation phase
- `[SDD-CONTEXT:constitution]` - Referencing project principles
- `[SDD-CONTEXT:spec]` - Referencing requirements
- `[SDD-CONTEXT:plan]` - Referencing architecture
- `[SDD-CONTEXT:tasks]` - Referencing task breakdown

### Enhanced Chat Patterns

#### Context-Rich Specification Requests
```
@workspace [SDD-PHASE:specify] Working on user authentication feature.
Context files: memory/constitution.md (security principles), current spec.md draft
Requirements: Secure login, password reset, 2FA support
Help me: Complete the specification following our SDD template structure
Consider: GDPR compliance from constitution, existing user model patterns
```

#### Architecture-Aware Planning Requests  
```
@workspace [SDD-PHASE:plan] Planning microservices architecture for e-commerce.
Context files: specs/feature-*/spec.md (requirements), memory/constitution.md (principles)
Tech stack preference: Node.js, PostgreSQL, Redis, Docker
Help me: Generate technical implementation plan with data model and API contracts
Consider: Scalability requirements from spec, performance standards from constitution
```

#### Implementation with Full Context
```
@workspace [SDD-PHASE:implement] Implementing UserService from task C2-1.
Context files: plan.md (architecture), data-model.md (User entity), tasks.md (current task)
Current task: Create UserService with CRUD operations and validation
Help me: Generate the service class following our established patterns
Consider: Error handling patterns from plan, validation rules from data model
```

### Reference Documentation Structure

#### Core Documentation Files
- `README.md` - Project overview and quick start
- `README-copilot.md` - Copilot-specific usage guide
- `AGENTS.md` - Multi-agent development guide
- `.github/copilot-instructions.md` - Detailed chat instructions

#### Development Resources
- `docs/` - Comprehensive documentation
- `templates/` - File templates and examples
- `scripts/` - Automation and workflow scripts
- `memory/` - Project context and principles

#### VSCode Integration Files
- `.vscode/settings.json` - Optimized Copilot settings
- `.vscode/tasks.json` - SDD workflow tasks
- `.vscode/spec-driven-dev.code-snippets` - Quick templates
- `.vscode/extensions.json` - Recommended extensions
- `spec-driven-development.code-workspace` - Workspace configuration

### Advanced Context Sharing

#### File Content Relationships
When analyzing code or providing suggestions, consider these relationships:

1. **Constitution → All Files**: Project principles apply to all development
2. **Spec → Plan**: Technical decisions must align with requirements
3. **Plan → Tasks**: Task breakdown must match architectural approach
4. **Tasks → Implementation**: Code must fulfill specific task requirements
5. **Implementation → Spec**: Final validation against original requirements

#### Cross-Reference Validation Patterns
- Validate implementations against specification requirements
- Ensure architectural decisions align with project principles
- Check task completion against acceptance criteria
- Verify code patterns match established conventions
- Confirm documentation stays current with implementation

### Model Context Protocol (MCP) Integration Points

#### Context Providers
- **File System Context**: Understand project structure and file relationships
- **Git Context**: Track changes and development history
- **Workspace Context**: Leverage VSCode workspace intelligence
- **Documentation Context**: Reference internal and external documentation

#### Context Consumers
- **Code Generation**: Use full project context for better suggestions
- **Documentation**: Generate context-aware documentation
- **Testing**: Create tests that align with specifications
- **Refactoring**: Suggest improvements considering project patterns

#### Context Protocols
- **Temporal Context**: Understanding development phase and history
- **Semantic Context**: Grasping project concepts and domain knowledge
- **Structural Context**: Recognizing architectural patterns and relationships
- **Procedural Context**: Following SDD methodology and workflows

This enhanced context enables GitHub Copilot to provide more intelligent, project-aware assistance throughout the Spec-Driven Development lifecycle.