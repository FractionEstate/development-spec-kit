# Spec-Driven Development with GitHub Copilot

GitHub Copilot is the primary partner in this repository. The playbook below distills the Spec-Driven Development (SDD) workflow, so every prompt, command, and artifact lands exactly where it should—no guesswork, no loose ends.

## � Quick Orientation

| What | Where | Why it Matters |
|------|-------|----------------|
| Project Constitution | `.specify/memory/constitution.md` | Non-negotiable principles that anchor every decision and review. |
| Active Feature Artifacts | `.specify/specs/<feature>/` | Canonical source for `spec.md`, `plan.md`, `tasks.md`, plus optional data models, contracts, and research. |
| Copilot System Prompts | `.github/copilot-instructions.md` & `.github/copilot-context.md` | Chat guidance that keeps Copilot aligned with SDD patterns and canonical paths. |
| Reference Library | `.github/copilot-references.md` | Curated links, checklists, and deep dives to accelerate answers. |
| VS Code Enhancements | `.vscode/` | Settings, tasks, and snippets tailored for the SDD workflow. |

## �️ Workspace Layout

```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md                 # Project-wide guardrails
│   └── specs/
│       └── <feature-slug>/
│           ├── spec.md                     # Feature specification
│           ├── plan.md                     # Architecture and sequencing
│           ├── tasks.md                    # Ordered implementation tasks
│           ├── data-model.md               # Entities and schemas (optional)
│           ├── contracts/                  # API or integration contracts (optional)
│           ├── quickstart.md               # Integration smoke tests (optional)
│           └── research.md                 # Supporting analysis (optional)
├── .github/
│   ├── copilot-instructions.md             # Primary Copilot briefing
│   ├── copilot-context.md                  # Ready-to-paste context patterns
│   ├── copilot-references.md               # Extended references and links
│   └── prompts/                            # Slash-command prompt set
└── .vscode/
    ├── settings.json                       # Copilot-optimized editor configuration
    ├── tasks.json                          # Workflow wiring for VS Code tasks
    └── spec-driven-dev.code-snippets       # Context-aware template snippets
```

## 🧭 Workflow Phases

1. **Constitution (`/constitution`)** – Establish principles, definition of done, and tooling expectations.
2. **Specify (`/specify`)** – Translate intent into a structured `spec.md` with acceptance criteria.
3. **Clarify (`/clarify`)** – Resolve open questions before any planning or coding begins.
4. **Plan (`/plan`)** – Produce the technical blueprint, sequencing, and risk callouts in `plan.md`.
5. **Tasks (`/tasks`)** – Break work into ordered, testable units stored in `tasks.md`.
6. **Implement (`/implement`)** – Code against the plan while updating task state and capturing deltas.
7. **Analyze (`/analyze`)** – Reconcile artifacts, surface gaps, and confirm readiness to ship.

Each slash command produces markdown artifacts directly inside `.specify/specs/<feature>/`, keeping the project audit-ready.

### Feature Bootstrap Walkthrough

| Step | Command / Artifact | What to Provide | Output |
|------|--------------------|-----------------|--------|
| 0 | Gather Intent | Raw narrative, goals, constraints | Starting context for the feature |
| 1 | `/specify` | Intent + constraints | `.specify/specs/<feature>/spec.md` with `[NEEDS CLARIFICATION]` markers |
| 2 | `/clarify` | Answers to each marker | Updated `spec.md` without blockers |
| 3 | `/plan` | Tech stack preferences, architectural guardrails | `plan.md`, optional `data-model.md`, risk notes |
| 4 | `/tasks` | Confirmation the plan is stable | `tasks.md` outlining ordered work (with `[P]` parallel items) |
| 5 | `/implement` | Reference to specific task IDs and plan sections | Implementation PRs plus updated `tasks.md` statuses |
| 6 | `/analyze` | Pointers to spec/plan/tasks | Gap report ensuring alignment before reviews |

Use this loop for every feature: intent → spec → clarifications → plan → tasks → implementation → analysis. Update the authoritative artifact after each step so Copilot never operates on stale context.

## 💬 Copilot Chat Playbook

### Guiding Principles

- **Lead with context.** Always point Copilot at the relevant `spec.md`, `plan.md`, `tasks.md`, and `constitution.md`.
- **Reference paths verbatim.** Use `.specify/specs/<feature>/…` so Copilot never confuses legacy directories.
- **Close the loop.** When Copilot proposes changes, update the authoritative artifact (spec, plan, tasks) before moving on.

### @workspace Templates

**Specification Upgrade**
```
@workspace I'm refining .specify/specs/<feature>/spec.md.
Current state: [summarize sections or gaps].
Request: Tighten acceptance criteria for [specific area] while honoring constitution.md requirements.
```

**Implementation Session**
```
@workspace Implementing [component] for .specify/specs/<feature>/tasks.md step [ID].
Plan reference: .specify/specs/<feature>/plan.md section [anchor].
Request: Generate code that satisfies [requirement] with tests outlined in tasks.md.
```

**Debugging & Analysis**
```
@workspace Investigating [issue] in [file or module].
Compare against: spec.md expectations + plan.md architecture for <feature>.
Request: Identify likely discrepancies and recommend updates to spec/plan/tasks if needed.
```

### Quick Context Snippets

- `spec-template` – Full specification scaffold with sections for scope, requirements, and validation.
- `copilot-context` – Ready-to-send context bundle for Copilot Chat.
- `sdd-chat` – Rich prompt skeleton optimized for multi-phase conversations.

## ⚡ Slash Commands & VS Code Tasks

| Slash Command | Purpose | When to Run | VS Code Task |
|---------------|---------|-------------|--------------|
| `/specify` | Generate or evolve a feature specification | Kick off a new feature or overhaul unclear requirements | **Specify: Create Feature** |
| `/clarify` | Resolve ambiguities flagged by `/specify` or reviewers | Before planning if any `[NEEDS CLARIFICATION]` markers remain | **Clarify: Resolve Ambiguities** |
| `/plan` | Produce architecture, sequencing, and risk notes | After the spec is stable and clarifications are settled | **Plan: Generate Implementation Plan** |
| `/tasks` | Derive actionable, ordered tasks | Immediately after planning to prepare implementation checkpoints | **Tasks: Generate Task Breakdown** |
| `/implement` | Execute coding work inline with the plan | While building; run iteratively per task cluster | **Implement: Execute Implementation** |
| `/analyze` | Cross-audit artifacts for drift or omissions | After major feature milestones or before reviews | **Analyze: Cross-Artifact Analysis** |
| `/constitution` | Establish or refine project principles | During project inception or governance updates | **Constitution: Set Project Principles** |

### VS Code Enhancements

- Copilot is enabled for every supported language with tuned completions.
- File nesting groups `spec.md`, `plan.md`, `tasks.md`, and related artifacts for fast navigation.
- Workspace search excludes build output, spotlighting only authoritative documents.
- Tasks (⇧⌘B / Ctrl+Shift+B) echo the slash commands so keyboard workflows stay fluid.
- Snippets mirror the latest templates—type the prefix, press **Tab**, and start drafting.

Tip: For a full list of task labels mapped to slash commands, see the “VS Code Tasks Cheat Sheet” in `.github/copilot-references.md`.

<a id="agent-tools--capabilities"></a>
## 🧰 Agent tools & capabilities

Your chat agent can use a focused toolkit to operate on this workspace. Mention the capability explicitly in your prompt when you need it.

| Capability | What it does | Typical prompt | Notes/limits |
|-----------|---------------|----------------|--------------|
| File edits & creation | Create or modify files anywhere in the repo | "Create `.specify/specs/<feature>/spec.md` with sections X/Y/Z" | Keeps changes minimal; preserves style; won’t run code unless asked |
| Workspace search | Find code/docs by keywords or semantics | "Search for references to 'tasks.md' across the repo and summarize" | Prefer broader queries, then narrow; avoids noisy outputs |
| Targeted file reads | Read large, meaningful chunks of files | "Open `templates/.github/copilot-instructions.md` and extract the workflow table" | Reads by line range to stay efficient |
| Terminal commands | Run one-line shell commands and summarize results | "Run git status -sb and report modified files" | No secrets; single-line commands; long outputs are truncated |
| VS Code tasks | Launch configured tasks that mirror slash commands | "Run the Tasks: Generate Task Breakdown" | Requires tasks.json wiring (see `.vscode/tasks.json`) |
| Snippets | Insert ready-made templates into docs | "Insert the `feature-bootstrap` checklist here" | See `.vscode/spec-driven-dev.code-snippets` |
| Notebooks (optional) | Edit or run Jupyter notebook cells | "Open the first code cell in `<notebook>.ipynb` and run it" | Only if notebooks exist in this repo |
| Browser preview (optional) | Open URLs in the editor’s simple browser | "Open the docs site URL and confirm the sidebar renders" | For quick previews; not a full browser |
| Session TODO tracking | Maintain a visible plan during multi-step work | "Start a TODO list with items A/B/C and mark A in-progress" | Keeps one item in progress at a time |

Tips
- Say what tool to use: "use the terminal", "edit the file", "search the workspace".
- Point to exact files/paths and desired outcomes.
- Ask for summaries and diffs to keep context tight.

<a id="try-it-5-minute-tour"></a>
## ⏱️ Try it: 5‑minute tour

Use these bite‑size prompts to exercise the most useful agent tools right away:

1) Workspace search → summary
- Prompt: "Search the workspace for 'Feature Bootstrap Walkthrough' and list files and headings where it appears. Then suggest any missing cross‑links."
- Outcome: A quick map of where the walkthrough lives and if more links are needed.

2) Targeted file read → extraction
- Prompt: "Open `templates/.github/copilot-instructions.md` and summarize the 'Prompt Quick Reference' table into 3 bullets."
- Outcome: A concise distillation you can paste into planning notes.

3) Terminal check → repo status
- Prompt: "Run `git status -sb` from the repo root and report any modified files grouped by directory."
- Outcome: A short status with zero noise; long outputs are auto‑truncated.

4) Session TODO tracking → visible plan
- Prompt: "Start a TODO list for today's session with: A) Review README sections, B) Add a demo clip link, C) Open a docs issue. Mark A in‑progress."
- Outcome: A structured plan with exactly one item in progress at a time.

5) Snippet insertion → instant scaffolding
- Prompt: "Insert the `agent-tools` snippet right below this line to show capabilities inline."
- Outcome: A reusable tools overview appears in place.

Notes
- Keep prompts explicit: name the tool, the file path(s), and the exact output you want.
- For notebook or browser preview actions, mention them explicitly (only if your repo includes those assets).

## �️ Quality Guardrails

### Code & Implementation
- Respect testing directives from `constitution.md` and `tasks.md`.
- Implement only what `spec.md` mandates; capture stretch ideas in `research.md`.
- Bake in logging, error handling, and observability defined in the plan.

### Documentation & Alignment
- Keep `plan.md` synchronized with architectural decisions made during implementation.
- Update `tasks.md` as progress unfolds—mark done, add blockers, track dependencies.
- Ensure terminology stays consistent across spec, plan, tasks, and code.

### Governance & Reviews
- Reference constitution excerpts when negotiating trade-offs.
- Run `/analyze` before handoffs to surface mismatches early.
- Record follow-up actions in the relevant artifact, not ad-hoc notes.

## 🧪 Troubleshooting Patterns

**Specification Ambiguity**
```
@workspace .specify/specs/<feature>/spec.md leaves [scenario] undefined.
Help me propose acceptance criteria and edge cases that satisfy constitution.md.
```

**Implementation Drift**
```
@workspace Compare current [component] implementation against spec.md + plan.md for <feature>.
Flag any mismatches and suggest updates to tasks.md to realign.
```

**Integration or Contract Breakage**
```
@workspace Validate [API integration] against .specify/specs/<feature>/contracts/[name].
Highlight contract clauses my current implementation violates and how to fix them.
```

**Task Hygiene**
```
@workspace Review .specify/specs/<feature>/tasks.md.
Mark [completed items], reprioritize remaining work, and note any blockers requiring clarification.
```

## 📚 Resource Hub

- **Primary Instructions** – `.github/copilot-instructions.md`
- **Context Playbook** – `.github/copilot-context.md`
- **Reference Library** – `.github/copilot-references.md`
- **VS Code Snippets** – `.vscode/spec-driven-dev.code-snippets`
- **Workflow Tasks** – `.vscode/tasks.json`

Stay disciplined about context, update the canonical artifacts first, and GitHub Copilot will deliver premium-quality assistance on every feature.
