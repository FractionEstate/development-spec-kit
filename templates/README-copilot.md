# Spec-Driven Development with GitHub Copilot

This project is optimized for **GitHub Copilot** and **VSCode Chat** integration. It follows the Spec-Driven Development (SDD) methodology where specifications drive implementation.

## 🚀 Getting Started with Copilot

### VSCode Setup
This project includes optimized VSCode configuration:
- ✅ Enhanced Copilot settings for all file types
- ✅ Spec-driven development file associations
- ✅ Code snippets for common templates
- ✅ Task integration for workflow commands
- ✅ File nesting for better organization

### GitHub Copilot Chat Optimization
The project includes `.github/copilot-instructions.md` with:
- 📋 Project context and structure explanation
- 🎯 Best practices for @workspace conversations
- 🔧 Integration features and shortcuts
- 🎨 Chat patterns for different development phases

## 📁 Project Structure

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
├── .vscode/
│   ├── settings.json           # Copilot-optimized settings
│   ├── tasks.json              # SDD workflow tasks
│   └── spec-driven-dev.code-snippets  # Quick templates
└── .github/
    ├── copilot-instructions.md # Chat optimization guide
    └── prompts/                # Enhanced command prompts
```

## 🎯 Spec-Driven Development Workflow

### 1. Constitution (`/constitution`)
Define your project's governing principles and development standards.

### 2. Specify (`/specify`)
Create detailed feature specifications from natural language descriptions.

### 3. Clarify (`/clarify`)
Resolve ambiguities and edge cases in your specifications.

### 4. Plan (`/plan`)
Generate technical implementation plans with architecture and tech stack.

### 5. Tasks (`/tasks`)
Break down the plan into actionable, granular tasks.

### 6. Implement (`/implement`)
Execute the implementation following the structured task plan.

### 7. Analyze (`/analyze`)
Validate consistency and completeness across all artifacts.

## 💬 Copilot Chat Best Practices

### Using @workspace Effectively

**For Specification Writing:**
```
@workspace I'm working on the user authentication specification.
Current spec.md has login/logout flows defined.
Please help me add password reset functionality while following our constitution.md security principles.
```

**For Implementation:**
```
@workspace I need to implement the UserService class from tasks.md.
The plan.md specifies Node.js with Express and MongoDB.
Please generate the code following our architecture patterns.
```

**For Debugging:**
```
@workspace I'm having authentication issues with the login endpoint.
Based on our spec.md requirements and plan.md architecture,
what could be causing the JWT token validation to fail?
```

### Quick Context Snippets
Use these snippets in markdown files:
- `copilot-context` - Basic context template
- `sdd-chat` - Enhanced chat request template
- `spec-template` - Complete feature specification template

## 🔧 VSCode Integration Features

### Available Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- **Specify: Create Feature** - Launch `/specify` command
- **Plan: Generate Implementation Plan** - Launch `/plan` command
- **Tasks: Generate Task Breakdown** - Launch `/tasks` command
- **Implement: Execute Implementation** - Launch `/implement` command
- **Constitution: Set Project Principles** - Launch `/constitution` command
- **Clarify: Resolve Ambiguities** - Launch `/clarify` command
- **Analyze: Cross-Artifact Analysis** - Launch `/analyze` command

### Enhanced File Organization
- Related files are nested together in the explorer
- Spec files are grouped with their implementation artifacts
- Enhanced search excludes build artifacts and dependencies
- Markdown preview optimized for specification documents

### Code Snippets
- `spec-template` - Complete feature specification
- `copilot-context` - Structured context for Copilot Chat
- `sdd-chat` - Enhanced chat request template

## 🎨 Chat Patterns by Phase

### During Specification
```
@workspace Working on [feature-name] specification.
Current context: Early specification phase
Files: spec.md (in progress)

Help me: [specific specification question]
Consider: Project constitution and user experience principles
```

### During Planning
```
@workspace Planning implementation for [feature-name].
Current context: Technical planning phase
Files: spec.md (complete), plan.md (in progress)

Help me: [architecture/technology question]
Consider: Specification requirements and project constraints
```

### During Implementation
```
@workspace Implementing [specific-component] for [feature-name].
Current context: Development phase
Files: spec.md, plan.md, tasks.md, [relevant-code-files]

Help me: [specific coding question]
Consider: Architecture from plan.md and requirements from spec.md
```

## 🛠️ Development Guidelines

### Code Quality
- Follow testing requirements from `constitution.md`
- Implement comprehensive error handling
- Include appropriate logging and monitoring
- Maintain clean, readable code structure

### Documentation
- Keep specifications current with implementation
- Update plans when making architectural changes
- Maintain task progress in `tasks.md`
- Document decisions in appropriate files

### Consistency
- Ensure spec-to-implementation alignment
- Maintain consistent terminology across files
- Follow established patterns and conventions
- Validate cross-file references and dependencies

## 🔍 Troubleshooting with Copilot

### Common Issues and Chat Patterns

**Specification Ambiguity:**
```
@workspace The current spec.md has unclear requirements for [specific area].
Help me clarify [specific ambiguity] and suggest concrete acceptance criteria.
```

**Implementation Drift:**
```
@workspace Compare my current [component] implementation against our spec.md requirements.
Are there any deviations from the specified behavior?
```

**Architecture Questions:**
```
@workspace Based on our plan.md architecture, what's the best way to implement [specific feature]?
Consider our tech stack: [list from plan.md]
```

**Task Management:**
```
@workspace Help me update tasks.md to reflect the completion of [completed tasks].
What should be the next priority based on our task dependencies?
```

## 📚 Additional Resources

- Read `.github/copilot-instructions.md` for comprehensive chat optimization guidance
- Review `.github/copilot-context.md` for enhanced context sharing patterns
- Explore `.github/copilot-references.md` for extensive documentation and reference links
- Use VSCode tasks for quick access to SDD workflow commands
- Reference code snippets for consistent formatting and structure
- Leverage file nesting for better project organization

**Enhanced Features:**
- 🔧 **Optimized Settings**: Streamlined VSCode configuration for better performance
- 🔗 **Reference Links**: Comprehensive documentation and resource links
- 📝 **Enhanced Snippets**: Improved code snippets with context-aware patterns
- 🎯 **Focused Context**: Streamlined context sharing for better AI understanding
- 📊 **Performance**: Optimized configurations for faster response times

Remember: GitHub Copilot Chat works best when provided with clear context about your current development phase, relevant files, and specific questions. Always reference the SDD workflow and project structure for optimal assistance.
