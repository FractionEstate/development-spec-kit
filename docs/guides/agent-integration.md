# Agent Integration Guide

This guide explains how automation agents, CI/CD pipelines, and scripts can consume `specify status` output.

## Overview

The `specify` CLI provides three output formats for the `status` command:

1. **Default** – Rich formatted tables with colors (human-friendly)
2. **JSON** – Complete structured data (best for complex automation)
3. **Agent** – Plain-text summary (optimized for AI agents and simple parsers)

## Agent Mode (`--agent`)

Agent mode provides a simplified, easy-to-parse plain-text format designed for AI assistants and automation scripts.

### Example Output

```text
NEXT_STEP: Kick off your first feature with /specify.
CONSTITUTION: ready
FEATURES: none (run /specify to create one)
COMMANDS: /analyze.prompt, /clarify.prompt, /constitution.prompt, /implement.prompt, /plan.prompt, /specify.prompt, /tasks.prompt, /update-constitution.prompt, /update-implement.prompt, /update-plan.prompt …
FOLLOWUPS:

- Kick off your first feature with /specify.

```text

### With Features

When features exist, the output includes detailed state for each:

```text
NEXT_STEP: Plan next steps with /plan → user-auth.
CONSTITUTION: ready
FEATURES:

- user-auth: spec=done plan=todo tasks=todo next=plan
- payment-flow: spec=done plan=done tasks=todo next=tasks
- dashboard: spec=done plan=done tasks=done next=implement

COMMANDS: /analyze.prompt, /clarify.prompt, /constitution.prompt, /implement.prompt, /plan.prompt, /specify.prompt, /tasks.prompt …
FOLLOWUPS:

- Plan next steps with /plan → user-auth.
- Create execution tasks via /tasks → payment-flow.
- Move into delivery with /implement → dashboard.

```text

### Parsing Agent Output

The format is designed for line-based parsing:

**Bash example:**

```bash

#!/bin/bash

output=$(specify status --agent)

# Extract next step

next_step=$(echo "$output" | grep "^NEXT_STEP:" | cut -d: -f2- | xargs)
echo "Next action: $next_step"

# Check constitution

constitution=$(echo "$output" | grep "^CONSTITUTION:" | cut -d: -f2 | xargs)
if [ "$constitution" = "ready" ]; then
    echo "✓ Constitution is recorded"
else
    echo "⚠ Constitution is missing"
fi

# Count features

feature_count=$(echo "$output" | grep "^- " | grep -c "spec=")
echo "Total features: $feature_count"

```text

**Python example:**

```python

#!/usr/bin/env python3

import subprocess
import re

def parse_agent_status():
    """Parse specify status --agent output."""
    result = subprocess.run(
        ["specify", "status", "--agent"],
        capture_output=True,
        text=True,
        check=True
    )

    lines = result.stdout.strip().split('\n')
    status = {
        'next_step': None,
        'constitution': None,
        'features': [],
        'commands': [],
        'followups': []
    }

    mode = None
    for line in lines:
        if line.startswith('NEXT_STEP:'):
            status['next_step'] = line.split(':', 1)[1].strip()
        elif line.startswith('CONSTITUTION:'):
            status['constitution'] = line.split(':', 1)[1].strip()
        elif line.startswith('FEATURES:'):
            mode = 'features'
        elif line.startswith('COMMANDS:'):
            mode = 'commands'
            commands_str = line.split(':', 1)[1].strip()
            status['commands'] = [
                cmd.strip() for cmd in commands_str.split(',')
            ]
        elif line.startswith('FOLLOWUPS:'):
            mode = 'followups'
        elif line.startswith('- ') and mode == 'features':
            # Parse: "- user-auth: spec=done plan=todo tasks=todo next=plan"
            match = re.match(r'- (\S+): spec=(\w+) plan=(\w+) tasks=(\w+) next=(\w+)', line)
            if match:
                status['features'].append({
                    'slug': match.group(1),
                    'spec': match.group(2),
                    'plan': match.group(3),
                    'tasks': match.group(4),
                    'next': match.group(5)
                })
        elif line.startswith('- ') and mode == 'followups':
            status['followups'].append(line[2:].strip())

    return status

# Usage

if __name__ == '__main__':
    status = parse_agent_status()
    print(f"Next step: {status['next_step']}")
    print(f"Constitution: {status['constitution']}")
    print(f"Features: {len(status['features'])}")

    for feature in status['features']:
        if feature['next'] == 'implement':
            print(f"✓ Ready to implement: {feature['slug']}")

```text

## JSON Mode (`--json`)

For complex integrations, use JSON mode to get complete structured data:

```bash
specify status --json

```text

### Example JSON Structure

```json
{
  "current_directory": "/path/to/project",
  "is_specify_project": true,
  "prompts": {
    "configured": true,
    "count": 12,
    "directory": "/path/to/project/.github/prompts",
    "commands": ["analyze.prompt", "clarify.prompt", "constitution.prompt", ...]
  },
  "model": {
    "selected_model": "gpt-4.1",
    "last_updated": "2025-10-03T12:34:56Z",
    "catalog_source": "api",
    "catalog_cached_at": "2025-10-03T12:30:00Z"
  },
  "scripts": {
    "preferred": "sh",
    "folder": "bash",
    "extension": ".sh",
    "last_updated": "2025-10-03T12:34:56Z"
  },
  "workflow": {
    "constitution": true,
    "features": [
      {
        "path": "/path/to/project/.specify/specs/user-auth",
        "slug": "user-auth",
        "spec": true,
        "plan": false,
        "tasks": false,
        "title": "User Authentication",
        "next_command": "plan",
        "ready_for_implementation": false
      }
    ],
    "feature_total": 1,
    "specs_ready": 1,
    "plans_ready": 0,
    "tasks_ready": 0,
    "waiting_plan": [...],
    "waiting_tasks": [],
    "missing_spec": []
  },
  "git": {
    "is_repo": true
  },
  "models_cache": {
    "path": "/home/user/.specify/models_cache.json",
    "age_seconds": 180,
    "source": "api",
    "timestamp": 1696337400.0
  },
  "followups": [
    "Plan next steps with /plan → user-auth."
  ],
  "next_suggestion": "Plan next steps with /plan → user-auth.",
  "config_error": null
}

```text

### JSON Parsing Example

**jq example:**

```bash

# Get next suggestion

specify status --json | jq -r '.next_suggestion'

# List all features needing plans

specify status --json | jq -r '.workflow.waiting_plan[].slug'

# Check if constitution exists

specify status --json | jq -r 'if .workflow.constitution then "ready" else "missing" end'

# Count ready-to-implement features

specify status --json | jq '.workflow.features | map(select(.ready_for_implementation)) | length'

```text

**Node.js example:**

```javascript
const { execSync } = require('child_process');

function getStatus() {
    const output = execSync('specify status --json', { encoding: 'utf8' });
    return JSON.parse(output);
}

const status = getStatus();

console.log(`Next step: ${status.next_suggestion}`);
console.log(`Features: ${status.workflow.feature_total}`);
console.log(`Ready for implementation: ${status.workflow.features.filter(f => f.ready_for_implementation).length}`);

// Find features that need work
const needsPlan = status.workflow.waiting_plan.map(f => f.slug);
const needsTasks = status.workflow.waiting_tasks.map(f => f.slug);

if (needsPlan.length > 0) {
    console.log(`\nNeeds planning: ${needsPlan.join(', ')}`);
}
if (needsTasks.length > 0) {
    console.log(`Needs tasks: ${needsTasks.join(', ')}`);
}

```text

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Check Spec Status

on:
  pull_request:
    branches: [main]

jobs:
  validate-specs:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v4

      - name: Install Specify CLI

        run: |
          curl -fsSL https://raw.githubusercontent.com/FractionEstate/development-spec-kit/main/scripts/bash/install-specify.sh | bash

      - name: Check project status

        run: |
          specify status --agent

          # Fail if constitution is missing
          if specify status --agent | grep -q "CONSTITUTION: missing"; then
            echo "❌ Constitution must be defined before merging"
            exit 1
          fi

          # Check for incomplete features
          incomplete=$(specify status --json | jq '.workflow.features | map(select(.spec == false or .plan == false or .tasks == false)) | length')
          if [ "$incomplete" -gt 0 ]; then
            echo "⚠️ $incomplete feature(s) have incomplete artifacts"
          fi

```text

### Pre-commit Hook Example

```bash

#!/bin/bash

# .git/hooks/pre-commit

specify status --agent > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️ Not a Specify project. Skipping spec validation."
    exit 0
fi

# Ensure constitution exists

if specify status --agent | grep -q "CONSTITUTION: missing"; then
    echo "❌ Constitution is required. Run /constitution in Copilot Chat."
    exit 1
fi

# Warn about incomplete specs

incomplete=$(specify status --json | jq '.workflow.missing_spec | length')
if [ "$incomplete" -gt 0 ]; then
    echo "⚠️ $incomplete feature(s) missing specs. Consider running /specify."
fi

exit 0

```text

## AI Agent Recommendations

When building AI agents that work with Specify projects:

1. **Always check `NEXT_STEP`** – This is the highest-priority action.
2. **Validate constitution first** – Most workflows require it.
3. **Follow the progression** – spec → plan → tasks → implement.
4. **Parse feature states** – Use the `next=` field to know what each feature needs.
5. **Use followups for context** – They provide additional guidance beyond the primary next step.
6. **Handle errors gracefully** – Check for "ERROR:" prefix in agent output.

### Example Agent Logic

```python
def suggest_next_action(status_output: str) -> str:
    """Generate a helpful suggestion based on Specify status."""

    if "ERROR:" in status_output:
        if "Not a Specify project" in status_output:
            return "This isn't a Specify project yet. Run 'specify init .' to get started."
        return "An error occurred. Check the status output."

    lines = status_output.split('\n')
    next_step = None
    constitution = None

    for line in lines:
        if line.startswith('NEXT_STEP:'):
            next_step = line.split(':', 1)[1].strip()
        elif line.startswith('CONSTITUTION:'):
            constitution = line.split(':', 1)[1].strip()

    if constitution == 'missing':
        return "Start by establishing project principles with /constitution."

    if next_step:
        # Remove rich formatting if present
        next_step = next_step.replace('[magenta]', '').replace('[/magenta]', '')
        return next_step

    return "Check 'specify status' for detailed project state."

```text

## Error Handling

### Not a Specify Project

```text
ERROR: Not a Specify project (missing .specify directory). Run 'specify init .' first.

```text

Exit code: 1

### Successful Status

Exit code: 0

All successful status commands return exit code 0, even if artifacts are incomplete. Use the output content to determine project health.

## Best Practices

1. **Use `--agent` for simple checks** – Fast parsing, minimal output.
2. **Use `--json` for detailed analysis** – Full feature lists, metadata, cache info.
3. **Cache JSON output** – If calling multiple times, save once and parse repeatedly.
4. **Check exit codes** – Non-zero means error (like missing .specify directory).
5. **Strip rich formatting** – Agent mode may contain `[magenta]...[/magenta]` tags in suggestions.
6. **Follow the workflow order** – Don't skip stages (spec before plan, plan before tasks).

## See Also

- [CLI Reference](cli.md) – Complete command documentation
- [Workflows](../workflows.md) – Detailed workflow descriptions
- [Quickstart](../getting-started/quickstart.md) – Getting started guide
