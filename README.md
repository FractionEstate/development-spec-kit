<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🚀 FractionEstate Development Spec Kit</h1>
    <h3><em>GitHub Models & VS Code optimized Spec-Driven Development</em></h3>
</div>

<p align="center">
    <strong>A specialized toolkit for FractionEstate teams to implement Spec-Driven Development using GitHub Models and VS Code, focusing on high-quality software delivery through AI-native workflows.</strong>
</p>

[![Release](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml)
[![Link Checker](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml)

---

## Table of Contents

- [🤔 What is Spec-Driven Development?](#-what-is-spec-driven-development)
- [⚡ Get started](#-get-started)
- [📽️ Video Overview](#️-video-overview)
- [🤖 GitHub Models Integration](#-github-models-integration)
- [🔧 Specify CLI Reference](#-specify-cli-reference)
- [📚 Core philosophy](#-core-philosophy)
- [🌟 Development phases](#-development-phases)
- [🎯 FractionEstate Goals](#-fractionestate-goals)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn more](#-learn-more)
- [📋 Detailed process](#-detailed-process)
- [🔍 Troubleshooting](#-troubleshooting)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

## 🤔 What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them.

## ⚡ Get started

### 1. Install Specify CLI

Install the FractionEstate Development Spec Kit CLI:

```bash
uv tool install specify-cli --from git+https://github.com/FractionEstate/development-spec-kit.git
```

Then use the tool directly:

```bash
specify init <PROJECT_NAME>
specify check
```

### 2. Initialize Your Project with GitHub Models

Create a new project optimized for GitHub Models and VS Code:

```bash
specify init my-project
```

Optionally pin a specific GitHub Model during initialization:

```bash
specify init my-project --model gpt-4o
```

This creates a project with:
- ✅ **VS Code Workspace Settings** - Optimized Copilot configuration
- ✅ **GitHub Models Instructions** - Project-specific guidance
- ✅ **Spec-Driven Workflows** - Structured development commands
- ✅ **VS Code Tasks & Snippets** - Integrated development experience

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

### 2. Establish project principles

Use the **`/constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

### 3. Create the spec

Use the **`/specify`** command to describe what you want to build. Focus on the **what** and **why**, not the tech stack.

```bash
/specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### 4. Create a technical implementation plan

Use the **`/plan`** command to provide your tech stack and architecture choices.

```bash
/plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### 5. Break down into tasks

Use **`/tasks`** to create an actionable task list from your implementation plan.

```bash
/tasks
```

### 6. Execute implementation

Use **`/implement`** to execute all tasks and build your feature according to the plan.

```bash
/implement
```

For detailed step-by-step instructions, see our [comprehensive guide](./spec-driven.md).

## 📽️ Video Overview

Want to see Spec Kit in action? Watch our [video overview](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)!

[![Spec Kit video header](/media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🤖 GitHub Models Integration

The FractionEstate Development Spec Kit is optimized specifically for **GitHub Models** and **VS Code**, providing enhanced features for specification-driven development:

### Enhanced Features for GitHub Models

| Feature | Description |
|---------|-------------|
| **VS Code Workspace Settings** | Optimized Copilot settings for all file types and enhanced AI assistance |
| **Chat-optimized Prompts** | Better @workspace conversation patterns for specification work |
| **Code Snippets** | Quick templates for specs, plans, and chat contexts |
| **Task Integration** | Run SDD commands directly from VS Code integrated terminal |
| **File Organization** | Smart nesting and associations for specification files |
| **Extensions** | Recommended VS Code extensions for optimal development experience |
| **Reference Links** | Comprehensive documentation and resource links |
| **Context Optimization** | Enhanced workspace intelligence for better AI suggestions |

### Key Files for GitHub Models
- `.vscode/settings.json` - Copilot-optimized workspace settings
- `.vscode/tasks.json` - Integrated SDD workflow tasks
- `.vscode/spec-driven-dev.code-snippets` - Quick templates and context patterns
- `.github/copilot-instructions.md` - Comprehensive chat guidance
- `.github/copilot-context.md` - Enhanced context sharing guide
- `.github/copilot-references.md` - Extensive documentation and reference links
- Enhanced command prompts in `.github/prompts/`

## 🔧 Specify CLI Reference

The `specify` command supports the following options:

### Commands

| Command     | Description                                                    |
|-------------|----------------------------------------------------------------|
| `init`      | Initialize a new Specify project optimized for GitHub Models  |
| `check`     | Check for installed tools (`git`, `code`/`code-insiders`) |

### `specify init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | Override the assistant profile (defaults to `copilot`; other values are legacy and not recommended) |
| `--model`              | Option   | Preselect a GitHub Model (e.g., `gpt-4o`, `gpt-4o-mini`)                    |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                 |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)  |
| `--ignore-agent-tools` | Flag     | Skip VS Code/GitHub Copilot tooling checks (useful in CI)                   |

### Examples

```bash
# Basic project initialization (defaults to GitHub Models)
specify init my-project

# Initialize with a specific GitHub Model
specify init my-project --model gpt-4o

# Initialize with PowerShell scripts (Windows/cross-platform)
specify init my-project --model gpt-4o --script ps

# Initialize in current directory
specify init .
# or use the --here flag
specify init --here

# Force merge into current (non-empty) directory without confirmation
specify init . --force
# or
specify init --here --force

# Skip git initialization
specify init my-project --no-git

# Enable debug output for troubleshooting
specify init my-project --debug

# Use GitHub token for API requests (helpful for corporate environments)
specify init my-project --github-token ghp_your_token_here
```

### Available Slash Commands

After running `specify init`, you can use these commands with GitHub Models Chat for structured development:

| Command         | Description                                                           |
|-----------------|-----------------------------------------------------------------------|
| `/constitution` | Create or update project governing principles and development guidelines |
| `/specify`      | Define what you want to build (requirements and user stories)        |
| `/clarify`      | Clarify underspecified areas (must be run before `/plan` unless explicitly skipped; formerly `/quizme`) |
| `/plan`         | Create technical implementation plans with your chosen tech stack     |
| `/tasks`        | Generate actionable task lists for implementation                     |
| `/analyze`      | Cross-artifact consistency & coverage analysis (run after /tasks, before /implement) |
| `/implement`    | Execute all tasks to build the feature according to the plan         |

### Environment Variables

| Variable         | Description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches.<br/>**Must be set in the context of the agent you're working with prior to using `/plan` or follow-up commands. |

## 📚 Core philosophy

Spec-Driven Development is a structured process that emphasizes:

- **Intent-driven development** where specifications define the "_what_" before the "_how_"
- **Rich specification creation** using guardrails and organizational principles
- **Multi-step refinement** rather than one-shot code generation from prompts
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

## 🌟 Development phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **0-to-1 Development** ("Greenfield") | Generate from scratch | <ul><li>Start with high-level requirements</li><li>Generate specifications</li><li>Plan implementation steps</li><li>Build production-ready applications</li></ul> |
| **Creative Exploration** | Parallel implementations | <ul><li>Explore diverse solutions</li><li>Support multiple technology stacks & architectures</li><li>Experiment with UX patterns</li></ul> |
| **Iterative Enhancement** ("Brownfield") | Brownfield modernization | <ul><li>Add features iteratively</li><li>Modernize legacy systems</li><li>Adapt processes</li></ul> |

## 🎯 FractionEstate Goals

This toolkit is designed to support FractionEstate's development objectives:

### GitHub-Centric Development

- Leverage GitHub Models' advanced AI capabilities for specification-driven development
- Integrate seamlessly with VS Code and GitHub's ecosystem
- Utilize GitHub's project management and CI/CD features

### Real Estate Technology Focus

- Build applications for real estate tokenization and fractional ownership
- Support complex financial calculations and regulatory compliance
- Enable scalable multi-tenant architecture for property management

### Enterprise-Grade Quality

- Demonstrate mission-critical application development practices
- Incorporate FractionEstate's technical standards and architectural patterns
- Support regulatory compliance and security requirements for financial applications

### Iterative & Collaborative Development

- Enable rapid prototyping and iteration cycles
- Support collaborative development with clear specifications
- Provide robust workflows for feature development and system modernization

## 🔧 Prerequisites

- **Linux/macOS** (or WSL2 on Windows)
- **[VS Code](https://code.visualstudio.com/)** with **[GitHub Copilot](https://github.com/features/copilot)** extension
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- Active GitHub Copilot subscription (required for AI assistance)

### Recommended VS Code Extensions
- GitHub Models
- GitHub Models Chat
- GitLens
- Python
- Markdown All in One

## 📖 Learn more

- **[Complete Spec-Driven Development Methodology](./spec-driven.md)** - Deep dive into the full process
- **[Detailed Walkthrough](#-detailed-process)** - Step-by-step implementation guide

---

## 📋 Detailed process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

You can use the Specify CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
specify init <project_name>
```

Or initialize in the current directory:

```bash
specify init .
# or use the --here flag
specify init --here
# Skip confirmation when the directory already has files
specify init . --force
# or
specify init --here --force
```

![Specify CLI bootstrapping a new project in the terminal](./media/specify_cli.gif)

The FractionEstate Development Spec Kit is optimized for GitHub Copilot. You can initialize with:

```bash
specify init <project_name>
# Include a specific GitHub Model if you prefer:
specify init <project_name> --model gpt-4o
# Or initialize in the current directory:
specify init .
# or use --here flag
specify init --here
# Force merge into a non-empty current directory
specify init . --force
# or
specify init --here --force
```

The CLI will check if you have VS Code installed and will set up GitHub Copilot-optimized configurations.

### **STEP 1:** Establish project principles

Go to the project folder and open it in VS Code. Start a new GitHub Copilot Chat session.

You will know that things are configured correctly if you see the spec-driven development prompts available in `.github/prompts/` and can use them in your Copilot Chat conversations.

The first step should be establishing your project's governing principles using the `/constitution` command. This helps ensure consistent decision-making throughout all subsequent development phases:

```text
/constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements. Include governance for how these principles should guide technical decisions and implementation choices.
```

This step creates or updates the `.specify/memory/constitution.md` file with your project's foundational guidelines that GitHub Copilot will reference during specification, planning, and implementation phases.

### **STEP 2:** Create project specifications

With your project principles established, you can now create the functional specifications. Use the `/specify` command and then provide the concrete requirements for the project you want to develop.

>[!IMPORTANT]
>Be as explicit as possible about _what_ you are trying to build and _why_. **Do not focus on the tech stack at this point**.

An example prompt:

```text
Develop Taskify, a team productivity platform. It should allow users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. In this initial phase for this feature,
let's call it "Create Taskify," let's have multiple users but the users will be declared ahead of time, predefined.
I want five users in two different categories, one product manager and four engineers. Let's create three
different sample projects. Let's have the standard Kanban columns for the status of each task, such as "To Do,"
"In Progress," "In Review," and "Done." There will be no login for this application as this is just the very
first testing thing to ensure that our basic features are set up. For each task in the UI for a task card,
you should be able to change the current status of the task between the different columns in the Kanban work board.
You should be able to leave an unlimited number of comments for a particular card. You should be able to, from that task
card, assign one of the valid users. When you first launch Taskify, it's going to give you a list of the five users to pick
from. There will be no password required. When you click on a user, you go into the main view, which displays the list of
projects. When you click on a project, you open the Kanban board for that project. You're going to see the columns.
You'll be able to drag and drop cards back and forth between different columns. You will see any cards that are
assigned to you, the currently logged in user, in a different color from all the other ones, so you can quickly
see yours. You can edit any comments that you make, but you can't edit comments that other people made. You can
delete any comments that you made, but you can't delete comments anybody else made.
```

After this prompt is entered, you should see GitHub Copilot kick off the planning and spec drafting process. The system will also trigger some of the built-in scripts to set up the repository.

Once this step is completed, you should have a new branch created (e.g., `001-create-taskify`), as well as a new specification in the `.specify/specs/001-create-taskify` directory.

The produced specification should contain a set of user stories and functional requirements, as defined in the template.

At this stage, your project folder contents should resemble the following:

```text
└── .specify
    ├── memory
    │	 └── constitution.md
    ├── scripts
    │	 ├── check-prerequisites.sh
    │	 ├── common.sh
    │	 ├── create-new-feature.sh
    │	 ├── setup-plan.sh
    │	 └── update-agent-context.sh
    ├── specs
    │	 └── 001-create-taskify
    │	     └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

### **STEP 3:** Functional specification clarification (required before planning)

With the baseline specification created, you can go ahead and clarify any of the requirements that were not captured properly within the first shot attempt.

You should run the structured clarification workflow **before** creating a technical plan to reduce rework downstream.

Preferred order:
1. Use `/clarify` (structured) – sequential, coverage-based questioning that records answers in a Clarifications section.
2. Optionally follow up with ad-hoc free-form refinement if something still feels vague.

If you intentionally want to skip clarification (e.g., spike or exploratory prototype), explicitly state that so the agent doesn't block on missing clarifications.

Example free-form refinement prompt (after `/clarify` if still needed):

```text
For each sample project or project that you create there should be a variable number of tasks between 5 and 15
tasks for each one randomly distributed into different states of completion. Make sure that there's at least
one task in each stage of completion.
```

You should also ask GitHub Copilot to validate the **Review & Acceptance Checklist**, checking off the things that are validated/pass the requirements, and leave the ones that are not unchecked. You can use this prompt in Copilot Chat:

```text
@workspace Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.
```

It's important to use the interaction with GitHub Copilot as an opportunity to clarify and ask questions around the specification - **do not treat its first attempt as final**.

### **STEP 4:** Generate a plan

You can now be specific about the tech stack and other technical requirements. You can use the `/plan` command that is built into the project template with a prompt like this:

```text
We are going to generate this using .NET Aspire, using Postgres as the database. The frontend should use
Blazor server with drag-and-drop task boards, real-time updates. There should be a REST API created with a projects API,
tasks API, and a notifications API.
```

The output of this step will include a number of implementation detail documents, with your directory tree resembling this:

```text
.
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   └── spec-driven-dev.code-snippets
└── .specify
    ├── memory
    │	 └── constitution.md
    ├── scripts
    │	 ├── check-prerequisites.sh
    │	 ├── common.sh
    │	 ├── create-new-feature.sh
    │	 ├── setup-plan.sh
    │	 └── update-agent-context.sh
    ├── specs
    │	 └── 001-create-taskify
    │	     ├── contracts
    │	     │	 ├── api-spec.json
    │	     │	 └── signalr-spec.md
    │	     ├── data-model.md
    │	     ├── plan.md
    │	     ├── quickstart.md
    │	     ├── research.md
    │	     └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

Check the `research.md` document to ensure that the right tech stack is used, based on your instructions. You can ask GitHub Copilot to refine it if any of the components stand out, or even have it check the locally-installed version of the platform/framework you want to use (e.g., .NET).

Additionally, you might want to ask GitHub Copilot to research details about the chosen tech stack if it's something that is rapidly changing (e.g., .NET Aspire, JS frameworks), with a prompt like this:

```text
I want you to go through the implementation plan and implementation details, looking for areas that could
benefit from additional research as .NET Aspire is a rapidly changing library. For those areas that you identify that
require further research, I want you to update the research document with additional details about the specific
versions that we are going to be using in this Taskify application and spawn parallel research tasks to clarify
any details using research from the web.
```

During this process, you might find that GitHub Copilot gets stuck researching the wrong thing - you can help nudge it in the right direction with a prompt like this:

```text
I think we need to break this down into a series of steps. First, identify a list of tasks
that you would need to do during implementation that you're not sure of or would benefit
from further research. Write down a list of those tasks. And then for each one of these tasks,
I want you to spin up a separate research task so that the net results is we are researching
all of those very specific tasks in parallel. What I saw you doing was it looks like you were
researching .NET Aspire in general and I don't think that's gonna do much for us in this case.
That's way too untargeted research. The research needs to help you solve a specific targeted question.
```

>[!NOTE]
>GitHub Copilot might be over-eager and add components that you did not ask for. Ask it to clarify the rationale and the source of the change.

### **STEP 5:** Have GitHub Copilot validate the plan

With the plan in place, you should have GitHub Copilot run through it to make sure that there are no missing pieces. You can use a prompt like this in Copilot Chat:

```text
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here. For example,
when I look at the core implementation, it would be useful to reference the appropriate places in the implementation
details where it can find the information as it walks through each step in the core implementation or in the refinement.
```

This helps refine the implementation plan and helps you avoid potential blind spots that GitHub Copilot missed in its planning cycle. Once the initial refinement pass is complete, ask GitHub Copilot to go through the checklist once more before you can get to the implementation.

You can also ask GitHub Copilot (if you have the [GitHub CLI](https://docs.github.com/en/github-cli/github-cli) installed) to go ahead and create a pull request from your current branch to `main` with a detailed description, to make sure that the effort is properly tracked.

>[!NOTE]
>Before you have GitHub Copilot implement it, it's also worth prompting it to cross-check the details to see if there are any over-engineered pieces (remember - it can be over-eager). If over-engineered components or decisions exist, you can ask GitHub Copilot to resolve them. Ensure that GitHub Copilot follows the [constitution](.specify/memory/constitution.md) as the foundational piece that it must adhere to when establishing the plan.

### STEP 6: Implementation

Once ready, use the `/implement` command to execute your implementation plan:

```text
/implement
```

The `/implement` command will:
- Validate that all prerequisites are in place (constitution, spec, plan, and tasks)
- Parse the task breakdown from `tasks.md`
- Execute tasks in the correct order, respecting dependencies and parallel execution markers
- Follow the TDD approach defined in your task plan
- Provide progress updates and handle errors appropriately

>[!IMPORTANT]
>GitHub Copilot will execute local CLI commands (such as `dotnet`, `npm`, etc.) - make sure you have the required tools installed on your machine.

Once the implementation is complete, test the application and resolve any runtime errors that may not be visible in CLI logs (e.g., browser console errors). You can copy and paste such errors back to GitHub Copilot Chat for resolution.

</details>

---

## 🔍 Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

## 👥 Maintainers

- Den Delimarsky ([@localden](https://github.com/localden))
- John Lam ([@jflam](https://github.com/jflam))

## 💬 Support

For support, please open a [GitHub issue](https://github.com/FractionEstate/development-spec-kit/issues/new). We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

## 🙏 Acknowledgements

This project is heavily influenced by and based on the work and research of [John Lam](https://github.com/jflam).

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
