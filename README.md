# Specify CLI - GitHub Copilot Spec-Driven Development Toolkit

[![Release](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml)
[![Link Checker](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml)

**Transform intent into implementation** with GitHub Copilot Chat, GitHub Models, and structured workflows.

## 🎯 What is Specify?

Specify is an opinionated toolkit that makes Spec-Driven Development practical. Instead of jumping straight to code, you:

1. **Define** project principles with `/constitution`
2. **Specify** features with `/specify`
3. **Plan** implementation with `/plan`
4. **Break down** work with `/tasks`
5. **Implement** with `/implement`

Every step is guided by GitHub Copilot Chat, powered by your choice of GitHub Models (GPT-4.1, Claude Sonnet 4.5, o3, and more).

## ⚡ Quick start

### Install

**Bash/Zsh:**

```bash
curl -fsSL https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/bash/install-specify.sh | bash
```

**PowerShell:**

```powershell
irm https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/powershell/install-specify.ps1 | iex
```

### Initialize project

```bash
# Create new project
specify init my-project --model claude-sonnet-4.5

# Or initialize current directory
specify init . --model gpt-4o
```

### Check status

```bash
specify status              # Rich formatted output
specify status --json       # Machine-readable JSON
specify status --agent      # Plain text for AI agents
```

## 📋 Available models

Specify supports **60+ GitHub Models** including:

| Family | Models |
|--------|--------|
| **OpenAI** | GPT-4.1, GPT-4.1 Mini, GPT-4o, GPT-4o Mini, GPT-5, o1, o3, o4-mini |
| **Anthropic (Claude)** | Claude Sonnet 4.5 ⭐, Claude Sonnet 4, Claude 3.7 Sonnet, Claude 3.5 Sonnet, Claude 3 Opus/Sonnet/Haiku |
| **Meta** | Llama 4 (Scout, Maverick), Llama 3.3, Llama 3.2 (Vision), Llama 3.1 |
| **Mistral** | Mistral Large, Mistral Medium, Mistral Small, Ministral, Codestral |
| **DeepSeek** | DeepSeek-R1, DeepSeek-V3 |
| **Microsoft** | Phi-4 (standard, mini, reasoning, multimodal) |
| **Others** | xAI Grok, Cohere Command, AI21 Jamba, and more |

> **Note:** Claude Sonnet 4.5 requires GitHub Copilot Pro/Business/Enterprise or BYOK (Bring Your Own Key).

View all models:

```bash
specify list-models
```

## 🔧 CLI commands

| Command | Purpose |
|---------|---------|
| `specify init` | Create or refresh a Specify project |
| `specify status` | View project status and next steps |
| `specify list-models` | Browse available GitHub Models |
| `specify check` | Validate prerequisites (Git, VS Code, Copilot) |
| `specify version` | Show CLI version and cache info |

**Full documentation:** [CLI Reference](docs/reference/cli.md)

## 📁 Project structure

After running `specify init`, your project will have:

```text
my-project/
├── .specify/                    # Core workflow engine
│   ├── memory/
│   │   └── constitution.md      # Project principles
│   ├── specs/                   # Feature specifications
│   │   └── <feature-name>/
│   │       ├── spec.md          # What to build
│   │       ├── plan.md          # How to build it
│   │       └── tasks.md         # Step-by-step breakdown
│   ├── scripts/                 # Automation scripts
│   └── templates/               # Document templates
│
├── .github/                     # GitHub Copilot configuration
│   ├── copilot-instructions.md  # Main Copilot guidance
│   ├── copilot-context.md       # Additional context
│   ├── copilot-references.md    # Reference documentation
│   └── prompts/                 # Slash commands
│       ├── constitution.prompt.md
│       ├── specify.prompt.md
│       ├── plan.prompt.md
│       ├── tasks.prompt.md
│       └── implement.prompt.md
│
└── .vscode/                     # VS Code settings
    ├── settings.json
    └── tasks.json
```

## 🤖 For AI agents and automation

Specify is designed to work seamlessly with AI agents. Use the `--agent` flag for plain-text output:

```bash
$ specify status --agent
NEXT_STEP: Plan next steps with /plan → user-auth.
CONSTITUTION: ready
FEATURES:
- user-auth: spec=done plan=todo tasks=todo next=plan
- dashboard: spec=done plan=done tasks=done next=implement
COMMANDS: /constitution, /specify, /plan, /tasks, /implement
FOLLOWUPS:
- Plan next steps with /plan → user-auth.
- Move into delivery with /implement → dashboard.
```

For complex integrations, use `--json` for structured data.

**Full guide:** [Agent Integration](docs/guides/agent-integration.md)

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [Overview](docs/overview.md) | High-level introduction |
| [Installation](docs/getting-started/installation.md) | Detailed setup instructions |
| [Quickstart](docs/getting-started/quickstart.md) | Get started in 5 minutes |
| [Workflows](docs/workflows.md) | Step-by-step workflow guide |
| [Agent Integration](docs/guides/agent-integration.md) | Using Specify with AI agents |
| [CLI Reference](docs/reference/cli.md) | Complete command documentation |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |

## 🎓 Core concepts

### Spec-Driven Development

The methodology behind Specify:

1. **Constitution** – Establish non-negotiable principles
2. **Specification** – Define what to build (outcomes, not implementation)
3. **Planning** – Break down how to build it
4. **Tasks** – Create executable work items
5. **Implementation** – Write code guided by specs

**Learn more:** [Spec-Driven Development Methodology](spec-driven.md)

### GitHub Models integration

Specify exclusively targets GitHub Models within GitHub Copilot:

- ✅ Fetches live model catalog from GitHub Models API
- ✅ Caches models locally (1-hour TTL)
- ✅ Falls back to curated list when API unavailable
- ✅ Includes Copilot-exclusive models (Claude Sonnet 4.5)
- ✅ Stores selection in `.specify/config/models.json`

**Technical details:** [GitHub Models Integration](AGENTS.md)

## 🚀 Workflow example

```bash
# 1. Create project
specify init todo-app --model claude-sonnet-4.5

# 2. Open in VS Code
cd todo-app
code .

# 3. In GitHub Copilot Chat:
@workspace /constitution
# Define project principles

@workspace /specify
# Create feature: user-authentication

@workspace /plan
# Break down implementation approach

@workspace /tasks
# Generate actionable work items

@workspace /implement
# Start coding with full context
```

## 🔐 Security

- **Credentials:** Never commit `.github/` if it contains API keys
- **Tokens:** Use environment variables (`GH_TOKEN`, `GITHUB_TOKEN`)
- **BYOK:** Claude models support Bring Your Own Key via Copilot

**Full policy:** [SECURITY.md](SECURITY.md)

## 🤝 Contributing

We welcome contributions! Please read:

- [CONTRIBUTING.md](CONTRIBUTING.md) – Development workflow
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) – Community standards
- [Local Development](docs/local-development.md) – Setup guide

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 💬 Support

- **Questions:** [Open a discussion](https://github.com/FractionEstate/development-spec-kit/discussions)
- **Bugs:** [File an issue](https://github.com/FractionEstate/development-spec-kit/issues)
- **Help:** See [SUPPORT.md](SUPPORT.md)

---

Made with ❤️ for developers who think before they code
