<div align="center">
    <img src="./media/logo.png" alt="FractionEstate Development Spec Kit logo" width="240" />
    <h1>FractionEstate Development Spec Kit</h1>
    <h3><em>Spec-Driven Development with GitHub Models + VS Code</em></h3>
</div>

<p align="center">
    <strong>Opinionated, GitHub Models–first tooling to build software from executable specs in VS Code.</strong>
</p>

[![Release](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/release.yml)
[![Link Checker](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml/badge.svg)](https://github.com/FractionEstate/development-spec-kit/actions/workflows/link-check.yml)

---

## Why this kit

This repo provides a small CLI and templates that make Spec‑Driven Development practical with GitHub Copilot Chat running on GitHub Models. It bootstraps a workspace, installs curated prompts, and wires VS Code for an AI‑native flow. Only GitHub Models are supported.

## 60‑second start

Install the CLI and initialize a project.

- bash/zsh:
    ```bash
    curl -fsSL https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/bash/install-specify.sh | bash && \
    specify init my-project && \
    specify check
    ```
- PowerShell:
    ```powershell
    iwr https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/powershell/install-specify.ps1 -UseBasicParsing | iex; specify init my-project; specify check
    ```

More options (update/uninstall, choose model/script): see ./docs/installation.md and ./docs/quickstart.md.

The install scripts automatically bootstrap [uv](https://docs.astral.sh/uv/) if it's not already on your PATH.

## What you get

Running `specify init` generates a VS Code–ready project with:

- GitHub Copilot Chat guidance under `.github/` (instructions, context, prompts)
- VS Code tasks/snippets for SDD flows
- Spec templates and a memory constitution starter
- GitHub Models selection (interactive or via `--model`)

<img src="./media/specify_cli.gif" alt="Specify CLI demo" width="700" />

## Usage

Initialize:

```bash
specify init <project-name>
```

Common options:

- `--model gpt-4o` preselects a GitHub Model
- `--script sh|ps` chooses shell script flavor (auto-detected otherwise)
- `--here` initializes in the current directory; combine with `--force` to merge into non-empty dirs
- `--no-git` skips repo init; `--github-token` supplies a token for private/preview models

Verify your environment:

```bash
specify check
```

## Work with specs in chat

After init, open VS Code and use GitHub Copilot Chat with these commands:

- `/constitution` – establish project principles (writes `.specify/memory/constitution.md`)
- `/specify` – describe what to build (requirements and user stories)
- `/clarify` – resolve gaps before planning
- `/plan` – produce the technical plan with your stack
- `/tasks` – generate actionable tasks
- `/analyze` – cross‑check coverage and consistency
- `/implement` – execute tasks to build the feature

## Agent capabilities (at a glance)

- Search/read workspace files, propose minimal diffs, and apply changes
- Run short terminal commands and summarize results
- Trigger VS Code tasks; insert curated prompt snippets
- Respect guardrails (no secrets, minimal/destructive changes confirmed)

See AGENTS.md for details.

## Documentation

- Quickstart: ./docs/quickstart.md
- Installation: ./docs/installation.md
- Methodology: ./spec-driven.md
- Project guide index: ./docs/index.md

## Contributing & Support

- Contributing guidelines: ./CONTRIBUTING.md
- Code of Conduct: ./CODE_OF_CONDUCT.md
- Support: ./SUPPORT.md
- Security: ./SECURITY.md

## License & Changelog

- License: ./LICENSE
- Changelog: ./CHANGELOG.md
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

## 💬 Support

For support, please open a [GitHub issue](https://github.com/FractionEstate/development-spec-kit/issues/new). We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
