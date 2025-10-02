# Spec Kit workflows

Every Spec Kit workspace ships with curated slash commands that keep GitHub Copilot Chat aligned with the Spec-Driven Development process. Each command reads and writes structured artifacts inside `.specify/` while respecting the project constitution.

## Command cheat sheet

| Command | Purpose | Primary outputs |
| ------- | ------- | ---------------- |
| `/constitution` | Establish non-negotiable principles, glossary, and guardrails | `.specify/memory/constitution.md` |
| `/specify` | Generate the baseline specification, user stories, and acceptance criteria | `.specify/specs/<feature>/spec.md` |
| `/clarify` | Resolve outstanding questions before planning | Clarifications appended to the spec |
| `/plan` | Produce the technical plan, data model, contracts, and quickstart | `.specify/specs/<feature>/plan.md` and supporting files |
| `/tasks` | Translate the plan into executable tasks with dependencies | `.specify/specs/<feature>/tasks.md` |
| `/analyze` | Audit spec/plan/tasks for coverage gaps and contradictions | Markdown analysis report (no file writes) |
| `/implement` | Execute the approved task list with guardrails and status updates | Code changes, tests, docs updates |

> Optional helpers such as `/research` or `/retro` can be added per-project, but the kit focuses on the core lifecycle above.

## Constitution

- **When**: Run immediately after scaffolding a new workspace.
- **Inputs**: Project vision, non-functional pillars, forbidden practices.
- **Outputs**: Structured constitution with articles, glossary, and amendment history.
- **Why it matters**: Every subsequent command references the constitution to enforce architectural discipline.

## Specify

- **Goal**: Capture requirements, user stories, acceptance criteria, open questions, and initial edge cases.
- **Artifacts**: Creates a numbered feature folder under `.specify/specs/`, complete with branch naming guidance.
- **Tips**: Focus on *what* and *why*; avoid implementation details. Mark ambiguities with `[NEEDS CLARIFICATION]`.

## Clarify

- **Goal**: Resolve outstanding `[NEEDS CLARIFICATION]` markers before planning.
- **Behavior**: Generates structured Q&A sections, updates the spec in-place, and records assumptions separately.
- **When to skip**: Only for spikes or exploratory prototypes where uncertainty is expected.

## Plan

- **Goal**: Translate the approved specification into an actionable architecture and delivery plan.
- **Outputs**: `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, and optional `research.md`.
- **Pre-flight gates**: The template enforces simplicity, anti-abstraction, and integration-first principles drawn from the constitution.

## Tasks

- **Goal**: Produce an execution-ready task list that TDD agents can consume.
- **Outputs**: `tasks.md` with IDs, dependencies, `[P]` parallel markers, and references to artifacts.
- **Quality hooks**: Flags tasks lacking requirements coverage and ensures test-first sequencing.

## Analyze (optional but recommended)

- **Goal**: Cross-check spec, plan, and tasks for inconsistencies before coding.
- **Result**: Markdown report highlighting coverage gaps, ambiguous requirements, terminology drift, and constitution conflicts. No files are mutated.
- **Usage**: Share the report with stakeholders or use it to drive refinements before `/implement`.

## Implement

- **Goal**: Execute the vetted tasks, drive tests red → green, and apply minimal diffs.
- **Safeguards**: Validates that constitution, spec, plan, and tasks all exist; enforces task order; surfaces progress updates.
- **Next steps**: Run local tests, push to a feature branch, and open a pull request.

## Supporting automation

- **CLI commands**: `specify status` summarizes configured prompts, script flavor, model choice, cache freshness, and now displays a workflow dashboard plus feature table that highlights which slash commands to run next. Use `--json` when you need automation-friendly output.
- **Scripts**: `.specify/scripts/**` provide Bash and PowerShell helpers used by the prompts to gather context.
- **Documentation**: Keep the [Quickstart](getting-started/quickstart.md) and [CLI reference](reference/cli.md) handy while you work through the lifecycle.
