#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import os
import subprocess  # nosec B404 - subprocess is required for CLI tool functionality
import sys
import zipfile
import tempfile
import shutil
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich import box
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)


def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def fetch_github_models(github_token: str = None, use_cache: bool = True) -> dict:
    """Fetch available GitHub Models from the API with optional caching."""
    cache_file = _models_cache_path()

    # Check cache first (if enabled and recent)
    if use_cache and cache_file.exists():
        try:
            cache_stat = cache_file.stat()
            # Use cache if less than 1 hour old
            if time.time() - cache_stat.st_mtime < 3600:  # 1 hour
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    if cached_data.get("models"):
                        return cached_data["models"]
        except Exception:  # nosec B110 - cache read errors should be silently ignored
            pass  # Ignore cache errors, continue with API fetch

    try:
        with httpx.Client(verify=ssl_context, timeout=10.0) as client:
            # Fetch from GitHub Models catalog API
            response = client.get(
                "https://models.github.ai/catalog/models",
                headers={
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                    **_github_auth_headers(github_token)
                }
            )
            if response.status_code == 200:
                models_data = response.json()

                # Combine API results with known GitHub Copilot models
                api_models = {}

                # Parse the models response and create a clean mapping
                if isinstance(models_data, list):
                    for model in models_data:
                        model_id = model.get("id", "")
                        model_name = model.get("name", model_id)
                        if model_id and "/" in model_id:  # Only process valid model IDs with publisher prefix
                            # Simplify model IDs (e.g., "openai/gpt-4o" -> "gpt-4o")
                            simple_id = model_id.split("/")[-1]
                            # Only add if it looks like a valid model ID (contains letters)
                            if simple_id and any(c.isalpha() for c in simple_id):
                                api_models[simple_id] = model_name

                # Merge: API models first, then add fallback models (so Copilot-exclusive models are included)
                fallback_models = get_fallback_github_models()
                combined_models = {**api_models, **fallback_models}

                # Save to cache for future use
                if use_cache:
                    try:
                        cache_file.parent.mkdir(parents=True, exist_ok=True)
                        cache_data = {
                            "models": combined_models,
                            "timestamp": time.time(),
                            "source": "api" if api_models else "fallback",
                        }
                        with open(cache_file, 'w') as f:
                            json.dump(cache_data, f, indent=2)
                    except Exception:  # nosec B110 - cache write errors should be silently ignored
                        pass  # Ignore cache save errors

                return combined_models
            else:
                # Fallback to known models if API fails
                fallback_only = get_fallback_github_models()
                if use_cache:
                    try:
                        cache_file.parent.mkdir(parents=True, exist_ok=True)
                        cache_file.write_text(
                            json.dumps(
                                {
                                    "models": fallback_only,
                                    "timestamp": time.time(),
                                    "source": "fallback",
                                },
                                indent=2,
                            )
                        )
                    except Exception:  # nosec B110 - cache write errors should be silently ignored
                        pass
                return fallback_only
    except Exception:
        # Fallback to known models if any error occurs
        fallback_only = get_fallback_github_models()
        if use_cache:
            try:
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(
                    json.dumps(
                        {
                            "models": fallback_only,
                            "timestamp": time.time(),
                            "source": "fallback",
                        },
                        indent=2,
                    )
                )
            except Exception:  # nosec B110 - cache write errors should be silently ignored
                pass
        return fallback_only

GITHUB_MODEL_FALLBACKS: dict[str, str] = {
    # OpenAI GPT-4.1 series
    "gpt-4.1": "GPT-4.1",
    "gpt-4.1-mini": "GPT-4.1 Mini",
    "gpt-4.1-nano": "GPT-4.1 Nano",

    # OpenAI GPT-4o series
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "gpt-4o-audio-preview": "GPT-4o Audio Preview",
    "gpt-4o-realtime-preview": "GPT-4o Realtime Preview",
    "gpt-4o-realtime-mini": "GPT-4o Realtime Mini",
    "gpt-4o-mini-transcribe": "GPT-4o Mini Transcribe",

    # OpenAI GPT-5 series (preview)
    "gpt-5": "GPT-5",
    "gpt-5-mini": "GPT-5 Mini",
    "gpt-5-nano": "GPT-5 Nano",
    "gpt-5-chat": "GPT-5 Chat (Preview)",

    # OpenAI o-series (reasoning models)
    "o1": "OpenAI o1",
    "o1-mini": "OpenAI o1-mini",
    "o1-preview": "OpenAI o1-preview",
    "o3": "OpenAI o3",
    "o3-mini": "OpenAI o3-mini",
    "o4-mini": "OpenAI o4-mini",

    # Anthropic Claude models (available in GitHub Copilot via native access or BYOK)
    # Model IDs match what appears in VS Code Copilot Chat model picker
    "claude-sonnet-4.5": "Claude Sonnet 4.5",
    "claude-4-sonnet": "Claude Sonnet 4",
    "claude-3-7-sonnet": "Claude Sonnet 3.7",
    "claude-3-5-sonnet": "Claude Sonnet 3.5",
    "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet (20241022)",
    "claude-3-opus": "Claude 3 Opus",
    "claude-3-sonnet": "Claude 3 Sonnet",
    "claude-3-haiku": "Claude 3 Haiku",

    # OpenAI embeddings
    "text-embedding-3-large": "Text Embedding 3 Large",
    "text-embedding-3-small": "Text Embedding 3 Small",
}
def get_fallback_github_models() -> dict:
    """Return a curated GitHub Models-only fallback list when the live catalog is unavailable."""
    return dict(GITHUB_MODEL_FALLBACKS)


def _models_cache_path() -> Path:
    return Path.home() / ".specify" / "models_cache.json"


def _load_models_cache_metadata() -> dict | None:
    cache_file = _models_cache_path()
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text())
        data["path"] = str(cache_file)
        data["age_seconds"] = max(time.time() - cache_file.stat().st_mtime, 0)
        return data
    except Exception:
        return {"path": str(cache_file), "age_seconds": None, "corrupt": True}


def _format_age(seconds: float | None) -> str:
    if seconds is None:
        return "unknown age"
    if seconds < 60:
        return f"{int(seconds)}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)}m"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)}h"
    days = hours / 24
    if days < 7:
        return f"{int(days)}d"
    weeks = days / 7
    return f"{int(weeks)}w"


def _parse_iso8601(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        cleaned = value.rstrip("Z") + "+00:00" if value.endswith("Z") else value
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


EM_DASH = "—"


def _read_first_markdown_heading(path: Path) -> str | None:
    """Return the first Markdown heading in a file, if present."""
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if stripped.startswith("#"):
                    return stripped.lstrip("# ").strip()
    except Exception:
        return None
    return None


def _collect_workflow_artifacts(specify_dir: Path) -> dict:
    """
    Inspect key workflow artifacts in a Specify workspace.

    Scans the .specify directory structure for constitution, specs, plans,
    and tasks, returning a comprehensive summary of workflow progress.

    Args:
        specify_dir: Path to the .specify directory

    Returns:
        Dictionary containing:
            - constitution (bool): Whether constitution.md exists
            - features (list[dict]): List of feature metadata
            - feature_total (int): Total number of features
            - specs_ready (int): Count of complete specs
            - plans_ready (int): Count of complete plans
            - tasks_ready (int): Count of complete tasks
            - waiting_plan (list[dict]): Features needing plans
            - waiting_tasks (list[dict]): Features needing tasks
            - missing_spec (list[dict]): Features without specs
    """
    constitution_path = specify_dir / "memory" / "constitution.md"
    constitution_exists = constitution_path.exists()

    specs_root = specify_dir / "specs"
    features: list[dict] = []

    if specs_root.exists():
        for feature_dir in sorted(specs_root.iterdir(), key=lambda p: p.name):
            if not feature_dir.is_dir():
                continue
            spec_path = feature_dir / "spec.md"
            plan_path = feature_dir / "plan.md"
            tasks_path = feature_dir / "tasks.md"

            spec_exists = spec_path.exists()
            plan_exists = plan_path.exists()
            tasks_exists = tasks_path.exists()

            if not spec_exists:
                next_command = "specify"
            elif not plan_exists:
                next_command = "plan"
            elif not tasks_exists:
                next_command = "tasks"
            else:
                next_command = "implement"

            features.append(
                {
                    "path": str(feature_dir),
                    "slug": feature_dir.name,
                    "spec": spec_exists,
                    "plan": plan_exists,
                    "tasks": tasks_exists,
                    "title": _read_first_markdown_heading(spec_path) if spec_exists else None,
                    "next_command": next_command,
                    "ready_for_implementation": next_command == "implement",
                }
            )

    specs_ready = sum(1 for feature in features if feature["spec"])
    plans_ready = sum(1 for feature in features if feature["plan"])
    tasks_ready = sum(1 for feature in features if feature["tasks"])

    waiting_plan = [feature for feature in features if feature["spec"] and not feature["plan"]]
    waiting_tasks = [feature for feature in features if feature["plan"] and not feature["tasks"]]
    missing_spec = [feature for feature in features if not feature["spec"]]

    return {
        "constitution": constitution_exists,
        "features": features,
        "feature_total": len(features),
        "specs_ready": specs_ready,
        "plans_ready": plans_ready,
        "tasks_ready": tasks_ready,
        "waiting_plan": waiting_plan,
        "waiting_tasks": waiting_tasks,
        "missing_spec": missing_spec,
    }


def _feature_display_name(feature: dict) -> str:
    """
    Format a feature name for display, combining slug and title.

    Args:
        feature: Feature metadata dict with 'slug' and 'title' keys

    Returns:
        Formatted display name (e.g., "my-feature · My Feature Title")
    """
    title = feature.get("title") or ""
    slug = feature.get("slug") or ""
    if title and title.lower() != slug.lower():
        return f"{slug} · {title}"
    return slug or title or "feature"


def _format_stage_progress(completed: int, total: int) -> str:
    """
    Format a progress indicator for workflow stages.

    Args:
        completed: Number of completed items
        total: Total number of items

    Returns:
        Colored rich-formatted progress string
    """
    if total == 0:
        if completed == 0:
            return "[yellow]Not started[/yellow]"
        return f"[green]{completed} ready[/green]"
    if completed == total:
        return f"[green]✓ {completed}/{total} ready[/green]"
    missing = total - completed
    return f"[yellow]{completed}/{total} ready[/yellow] ([red]{missing} pending[/red])"


def _derive_followups(summary: dict) -> list[str]:
    """
    Derive actionable follow-up suggestions based on workflow state.

    Analyzes the current state of constitution, features, specs, plans, and tasks
    to generate prioritized suggestions for the next workflow steps.

    Args:
        summary: Workflow artifact summary with keys:
            - constitution (bool): Whether constitution exists
            - specs_ready (int): Number of complete specs
            - missing_spec (list): Features without specs
            - waiting_plan (list): Features needing plans
            - waiting_tasks (list): Features needing tasks
            - features (list): All feature metadata

    Returns:
        List of formatted follow-up suggestions in priority order
    """
    followups: list[str] = []
    specs_ready = summary.get("specs_ready", 0)

    if not summary.get("constitution"):
        followups.append("Record guardrails with [magenta]/constitution[/magenta].")
    if specs_ready == 0:
        followups.append("Kick off your first feature with [magenta]/specify[/magenta].")
    if summary.get("missing_spec"):
        missing = summary["missing_spec"]
        names = ", ".join(_feature_display_name(feature) for feature in missing[:3])
        if len(missing) > 3:
            names += ", …"
        followups.append(f"Finish draft specs for: {names}.")
    if summary.get("waiting_plan"):
        waiting_plan = summary["waiting_plan"]
        names = ", ".join(_feature_display_name(feature) for feature in waiting_plan[:3])
        if len(waiting_plan) > 3:
            names += ", …"
        followups.append(f"Plan next steps with [magenta]/plan[/magenta] → {names}.")
    if summary.get("waiting_tasks"):
        waiting_tasks = summary["waiting_tasks"]
        names = ", ".join(_feature_display_name(feature) for feature in waiting_tasks[:3])
        if len(waiting_tasks) > 3:
            names += ", …"
        followups.append(f"Create execution tasks via [magenta]/tasks[/magenta] → {names}.")

    ready_for_impl = [feature for feature in summary.get("features", []) if feature.get("ready_for_implementation")]
    if ready_for_impl:
        names = ", ".join(_feature_display_name(feature) for feature in ready_for_impl[:3])
        if len(ready_for_impl) > 3:
            names += ", …"
        followups.append(f"Move into delivery with [magenta]/implement[/magenta] → {names}.")

    return followups


def _pick_primary_suggestion(summary: dict) -> str | None:
    """
    Select the single most important next action from workflow state.

    Returns the highest-priority suggestion for what the user should do next,
    based on completeness of constitution, specs, plans, and tasks.

    Args:
        summary: Workflow artifact summary dictionary

    Returns:
        Formatted suggestion string, or None if no suggestion available
    """
    followups = _derive_followups(summary)
    if followups:
        return followups[0]
    if summary.get("feature_total"):
        return "All core artifacts are ready. Consider running [magenta]/implement[/magenta] or opening a pull request."
    return "Start your first feature with [magenta]/specify[/magenta]."


def _render_workflow_summary(summary: dict) -> None:
    """
    Display formatted workflow artifacts summary table.

    Shows the status of constitution, specs, plans, and tasks with
    next-step guidance for incomplete stages.

    Args:
        summary: Workflow artifact summary containing stage completion data
    """
    console.print()
    table = Table(
        title="Workflow Artifacts",
        box=box.SIMPLE_HEAVY,
        show_edge=True,
        show_header=True,
        pad_edge=True,
    )
    table.add_column("Stage", style="cyan", no_wrap=True)
    table.add_column("Status", style="white")
    table.add_column("Next Step", style="magenta")

    constitution_status = (
        "[green]✓ Recorded[/green]" if summary["constitution"] else "[yellow]Missing[/yellow]"
    )
    constitution_next = (
        EM_DASH if summary["constitution"] else "Run [magenta]/constitution[/magenta] in Copilot Chat"
    )
    table.add_row("Constitution", constitution_status, constitution_next)

    feature_total = summary["feature_total"]
    specs_ready = summary["specs_ready"]

    if feature_total == 0:
        specs_status = "[yellow]No features captured yet[/yellow]"
    else:
        specs_status = (
            f"[green]✓ {specs_ready} feature{'s' if specs_ready != 1 else ''} captured[/green]"
            if specs_ready and specs_ready == feature_total
            else _format_stage_progress(specs_ready, feature_total)
        )
    specs_next = (
        EM_DASH
        if specs_ready
        else "Use [magenta]/specify[/magenta] to draft your first feature"
    )
    if summary["missing_spec"]:
        first_missing = summary["missing_spec"][0]
        specs_next = (
            f"Complete spec → [magenta]/specify[/magenta] · {_feature_display_name(first_missing)}"
        )
    table.add_row("Specs", specs_status, specs_next)

    plans_ready = summary["plans_ready"]
    plan_total = specs_ready if specs_ready else 0
    if specs_ready == 0:
        plans_status = "[dim]Waiting for specs[/dim]"
    else:
        plans_status = _format_stage_progress(plans_ready, plan_total)
    if summary["waiting_plan"]:
        next_feature = summary["waiting_plan"][0]
        plans_next = f"[magenta]/plan[/magenta] → {_feature_display_name(next_feature)}"
    elif plans_ready:
        plans_next = EM_DASH
    else:
        plans_next = "Run [magenta]/plan[/magenta] after [magenta]/specify[/magenta]"
    table.add_row("Plans", plans_status, plans_next)

    tasks_ready = summary["tasks_ready"]
    tasks_total = plans_ready if plans_ready else 0
    if plans_ready == 0:
        tasks_status = "[dim]Waiting for plans[/dim]"
    else:
        tasks_status = _format_stage_progress(tasks_ready, tasks_total)
    if summary["waiting_tasks"]:
        next_tasks = summary["waiting_tasks"][0]
        tasks_next = f"[magenta]/tasks[/magenta] → {_feature_display_name(next_tasks)}"
    elif tasks_ready:
        tasks_next = EM_DASH
    else:
        tasks_next = "Run [magenta]/tasks[/magenta] after [magenta]/plan[/magenta]"
    table.add_row("Tasks", tasks_status, tasks_next)

    console.print(table)

    followups = _derive_followups(summary)
    if followups:
        console.print()
        console.print("[dim]Next suggestions:[/dim]")
        for item in followups:
            console.print(f"  • {item}")


def _format_stage_cell(flag: bool) -> str:
    """
    Format a table cell showing stage completion status.

    Args:
        flag: Whether the stage is complete

    Returns:
        Colored checkmark (✓) for complete, circle (○) for incomplete
    """
    return "[green]✓[/green]" if flag else "[yellow]○[/yellow]"


def _next_action_label(feature: dict) -> str:
    """
    Generate a formatted label for the next required action on a feature.

    Args:
        feature: Feature metadata dict with 'next_command' key

    Returns:
        Formatted command suggestion or em dash if none needed
    """
    mapping = {
        "specify": "Draft with [magenta]/specify[/magenta]",
        "plan": "Plan via [magenta]/plan[/magenta]",
        "tasks": "Task with [magenta]/tasks[/magenta]",
        "implement": "Ready for [magenta]/implement[/magenta]",
    }
    return mapping.get(feature.get("next_command"), EM_DASH)


def _render_feature_details(summary: dict) -> None:
    """
    Display detailed feature progress table.

    Shows up to 5 features with their spec/plan/tasks completion status
    and suggested next action for each feature.

    Args:
        summary: Workflow artifact summary with feature list
    """
    features = summary.get("features") or []
    if not features:
        console.print()
        console.print("[dim]No feature folders yet. Use [magenta]/specify[/magenta] to start your first feature.[/dim]")
        return

    console.print()
    console.print("[bold]Feature Progress[/bold]")

    table = Table(box=box.SIMPLE, show_header=True, show_edge=True)
    table.add_column("Feature", style="cyan", no_wrap=True)
    table.add_column("Spec", justify="center")
    table.add_column("Plan", justify="center")
    table.add_column("Tasks", justify="center")
    table.add_column("Next Action", style="magenta")

    for feature in features[:5]:
        feature_name = _feature_display_name(feature)
        table.add_row(
            feature_name,
            _format_stage_cell(feature.get("spec")),
            _format_stage_cell(feature.get("plan")),
            _format_stage_cell(feature.get("tasks")),
            _next_action_label(feature),
        )

    console.print(table)

    if len(features) > 5:
        console.print(
            f"[dim]Showing first 5 of {len(features)} features. Run with --json to see the full list.[/dim]"
        )

# Constants
WORKSPACE_DOT_DIRS = (".github", ".vscode", ".specify")
AI_CHOICES = {
    "copilot": "GitHub Models",
}
# Add script type choices
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

# Agent configurations for setup (directory, format, arg placeholder)
agent_configs = {
    "copilot": {"dir": ".github/prompts", "format": "prompt.md", "arg_placeholder": "$ARGUMENTS"},
}



# ASCII Art Banner
BANNER = r"""
+===============================================================+
| _______ ______ _______ ______ _______ _______ _______ _______ |
||    ___|   __ \   _   |      |_     _|_     _|       |    |  ||
||    ___|      <       |   ---| |   |  _|   |_|   -   |       ||
||___|   |___|__|___|___|______| |___| |_______|_______|__|____||
|                                                               |
| _______ _______ _______ _______ _______ _______               |
||    ___|     __|_     _|   _   |_     _|    ___|              |
||    ___|__     | |   | |       | |   | |    ___|              |
||_______|_______| |___| |___|___| |___| |_______|              |
+===============================================================+
"""

TAGLINE = "GitHub Spec Kit - Spec-Driven Development Toolkit"
class StepTracker:
    """Track and render hierarchical steps without emojis in a clean tree format.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:  # nosec B110 - UI refresh errors should not crash the application
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree



MINI_BANNER = r"""
+===============================================================+
| _______ ______ _______ ______ _______ _______ _______ _______ |
||    ___|   __ \   _   |      |_     _|_     _|       |    |  ||
||    ___|      <       |   ---| |   |  _|   |_|   -   |       ||
||___|   |___|__|___|___|______| |___| |_______|_______|__|____||
|                                                               |
| _______ _______ _______ _______ _______ _______               |
||    ___|     __|_     _|   _   |_     _|    ___|              |
||    ___|__     | |   | |       | |   | |    ___|              |
||_______|_______| |___| |___|___| |___| |_______|              |
+===============================================================+
"""

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    # Arrow keys
    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'

    # Enter/Return
    if key == readchar.key.ENTER:
        return 'enter'

    # Escape
    if key == readchar.key.ESC:
        return 'escape'

    # Ctrl+C
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key



def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Falls back to default selection if not running in an interactive terminal.

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    # Check if we're in an interactive terminal
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        # Non-interactive mode: return default or first option
        if default_key and default_key in options:
            console.print(f"[dim]Non-interactive mode: using default '{default_key}'[/dim]")
            return default_key
        first_key = list(options.keys())[0]
        console.print(f"[dim]Non-interactive mode: using '{first_key}'[/dim]")
        return first_key

    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    # Suppress explicit selection print; tracker / later logic will report consolidated status
    return selected_key



console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    # Show banner only when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'specify --help' for usage information[/dim]"))
        console.print()


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True)  # nosec B603 - cmd is a list, shell=False
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return)  # nosec B603 - cmd is a list, shell=False
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool_for_tracker(tool: str, tracker: StepTracker) -> bool:
    """Check if a tool is installed and update tracker."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    else:
        tracker.error(tool, "not found")
        return False


def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""
    if shutil.which(tool):
        return True
    else:
        return False


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(  # nosec B603,B607 - git is a required dependency, input is controlled
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)  # nosec B603,B607 - git is required, no user input
        subprocess.run(["git", "add", "."], check=True, capture_output=True)  # nosec B603,B607 - git is required, no user input
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True)  # nosec B603,B607 - git is required, hardcoded message
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True

    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def fetch_latest_release_metadata(client: httpx.Client, github_token: str | None = None, debug: bool = False) -> dict:
    repo_owner = "FractionEstate"
    repo_name = "development-spec-kit"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    response = client.get(
        api_url,
        timeout=30,
        follow_redirects=True,
        headers=_github_auth_headers(github_token),
    )
    status = response.status_code
    if status != 200:
        msg = f"GitHub API returned {status} for {api_url}"
        if debug:
            msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
        raise RuntimeError(msg)
    try:
        release_data = response.json()
    except ValueError as je:
        raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    return release_data


def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")

    try:
        release_data = fetch_latest_release_metadata(client, github_token, debug)
    except Exception as e:
        console.print("[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    # Find the template asset for the specified AI assistant
    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print("[cyan]Downloading template...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"Download failed with {response.status_code}\nHeaders: {response.headers}\nBody (truncated): {body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print("[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata


def copy_local_template(project_path: Path, ai_assistant: str, script_type: str, selected_model: str = None, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None) -> Path:
    """Copy local development templates to create a new project for testing.
    Returns project_path. Uses tracker if provided (with keys: copy, agent-setup, cleanup)
    """
    # Find the development template directory
    dev_templates_dir = Path(__file__).parent.parent.parent / "templates"
    dev_memory_dir = Path(__file__).parent.parent.parent / "memory"
    dev_scripts_dir = Path(__file__).parent.parent.parent / "scripts"

    if not dev_templates_dir.exists():
        raise RuntimeError(f"Local templates directory not found: {dev_templates_dir}")

    if tracker:
        tracker.start("copy", "copying local templates")

    try:
        # Ensure project directory exists
        project_path.mkdir(parents=True, exist_ok=True)

        # Create .specify directory and copy development assets
        specify_dir = project_path / ".specify"
        specify_dir.mkdir(parents=True, exist_ok=True)

        # Copy memory
        if dev_memory_dir.exists():
            shutil.copytree(dev_memory_dir, specify_dir / "memory", dirs_exist_ok=True)

        # Copy scripts
        if dev_scripts_dir.exists():
            shutil.copytree(dev_scripts_dir, specify_dir / "scripts", dirs_exist_ok=True)

        # Copy templates to .specify/templates
        shutil.copytree(dev_templates_dir, specify_dir / "templates", dirs_exist_ok=True)

        # Copy VS Code workspace settings to project root
        vscode_src = dev_templates_dir / ".vscode"
        if vscode_src.exists():
            shutil.copytree(vscode_src, project_path / ".vscode", dirs_exist_ok=True)

        # Copy GitHub Copilot guidance (excluding prompts, which are regenerated)
        github_src = dev_templates_dir / ".github"
        github_dest = project_path / ".github"
        github_dest.mkdir(parents=True, exist_ok=True)

        if github_src.exists():
            for item in github_src.iterdir():
                if item.name == "prompts":
                    continue
                dest_path = github_dest / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_path, dirs_exist_ok=True)
                else:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)

        # Ensure prompts directory exists; contents will be generated below
        (github_dest / "prompts").mkdir(parents=True, exist_ok=True)

        if tracker:
            tracker.complete("copy", "local templates copied")
            tracker.add("agent-setup", "Set up agent commands")

        # Set up agent-specific commands
        setup_agent_commands(project_path, ai_assistant, script_type, selected_model, tracker)

        if tracker:
            tracker.complete("agent-setup", f"{ai_assistant} commands ready")

    except Exception as e:
        if tracker:
            tracker.error("copy", str(e))
        raise RuntimeError(f"Failed to copy local templates: {e}")

    return project_path
def setup_agent_commands(project_path: Path, ai_assistant: str, script_type: str, selected_model: str = None, tracker: StepTracker | None = None):
    """Set up GitHub Models-specific commands from templates."""
    if ai_assistant not in agent_configs:
        return  # Skip if no config defined

    config = agent_configs[ai_assistant]
    templates_dir = project_path / ".specify" / "templates" / "commands"
    output_dir = project_path / config["dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    script_folder_map = {"ps": "powershell", "sh": "bash"}
    script_extension_map = {"ps": "ps1", "sh": "sh"}
    script_folder = script_folder_map.get(script_type, script_type)
    script_extension = script_extension_map.get(script_type, script_type)

    # Persist configuration (model + script metadata) for status reporting
    if ai_assistant == "copilot":
        config_dir = project_path / ".specify" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / "models.json"
        existing: dict = {}
        if config_file.exists():
            try:
                existing = json.loads(config_file.read_text())
            except Exception:
                existing = {}

        config_payload = existing.copy()

        github_meta = config_payload.get("github_models", {})
        catalog_meta = _load_models_cache_metadata() or {}
        if selected_model:
            github_meta.update(
                {
                    "selected_model": selected_model,
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "catalog_source": catalog_meta.get("source") or github_meta.get("catalog_source", "user-selection"),
                }
            )
        elif catalog_meta.get("source") and "catalog_source" not in github_meta:
            github_meta["catalog_source"] = catalog_meta.get("source")

        if catalog_meta.get("timestamp") and "catalog_cached_at" not in github_meta:
            try:
                cached_dt = datetime.fromtimestamp(catalog_meta["timestamp"], tz=timezone.utc)
                github_meta["catalog_cached_at"] = cached_dt.isoformat()
            except Exception:  # nosec B110 - timestamp parsing errors should not crash status command
                pass
        config_payload["github_models"] = github_meta

        config_payload["scripts"] = {
            "preferred": script_type,
            "folder": script_folder,
            "extension": script_extension,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

        config_file.write_text(json.dumps(config_payload, indent=2))

    # Process each command template
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.md"):
            command_name = template_file.stem
            content = template_file.read_text()

            # Replace placeholders
            content = content.replace("$ARGUMENTS", config["arg_placeholder"])
            content = content.replace(
                "{SCRIPT}", f".specify/scripts/{script_folder}/{template_file.stem}.{script_extension}"
            )

            if config["format"] == "toml":
                # Wrap in TOML format
                description = content.split('\n', 1)[0].strip('# ').strip()  # Extract description from first line
                prompt_content = content.replace(f'# {description}', '', 1).strip()
                content = f'description = "{description}"\n\nprompt = """\n{prompt_content}\n"""'
                output_file = output_dir / f"{command_name}.toml"
            elif config["format"] == "prompt.md":
                output_file = output_dir / f"{command_name}.prompt.md"
            else:
                output_file = output_dir / f"{command_name}.md"

            output_file.write_text(content)


def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()

    # Step: fetch + download combined
    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        # Create project directory only if not using current directory
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in the ZIP for debugging
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            # For current directory, extract to a temp location first
            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    # Check what was extracted
                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    # Handle GitHub-style ZIP with a single root directory
                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print("[cyan]Found nested directory structure[/cyan]")

                    # Copy contents to current directory
                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                # Recursively copy directory contents
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print("[cyan]Template files merged into current directory[/cyan]")
            else:
                # Extract directly to project directory (original behavior)
                zip_ref.extractall(project_path)

                # Check what was extracted
                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                # Handle GitHub-style ZIP with a single root directory
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # Move contents up one level
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"
                    # Move the nested directory contents to temp location
                    shutil.move(str(nested_dir), str(temp_move_dir))
                    # Remove the now-empty project directory
                    project_path.rmdir()
                    # Rename temp directory to project directory
                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print("[cyan]Flattened nested directory structure[/cyan]")

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")
        # Clean up downloaded ZIP file
        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .specify/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:  # nosec B112 - file read errors should skip the file
                continue
            st = script.stat()
            mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400:
                new_mode |= 0o100
            if mode & 0o040:
                new_mode |= 0o010
            if mode & 0o004:
                new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")


def _merge_directory(source: Path, destination: Path) -> list[str]:
    """Merge source directory into destination, returning list of new relative paths copied."""
    copied: list[str] = []
    if not source.exists() or not source.is_dir():
        return copied

    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        target = destination / item.name
        if item.is_dir():
            child_results = _merge_directory(item, target)
            copied.extend([f"{item.name}/{child}" for child in child_results])
        else:
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied.append(item.name)
    return copied


def sync_workspace_config(project_path: Path, workspace_root: Path) -> tuple[bool, str]:
    """Ensure workspace root has required dot-directories for slash commands.

    Returns (changed, detail).
    """
    try:
        if project_path.resolve() == workspace_root.resolve():
            return False, "project is workspace root"
    except FileNotFoundError:
        return False, "workspace path missing"

    if not is_git_repo(workspace_root):
        return False, "workspace root not a git repo"

    synced_dirs: list[str] = []
    for dirname in WORKSPACE_DOT_DIRS:
        source = project_path / dirname
        if not source.exists():
            continue
        destination = workspace_root / dirname
        copied = _merge_directory(source, destination)
        if copied:
            synced_dirs.append(dirname)

    if not synced_dirs:
        return False, "no workspace directories to sync"

    detail = ", ".join(synced_dirs)
    return True, f"synced {detail}"


def resolve_workspace_root(start: Path) -> Path:
    """Return git workspace root if inside a repo, otherwise the starting path."""
    if is_git_repo(start):
        try:
            result = subprocess.run(  # nosec B603,B607 - git is required, input is controlled
                ["git", "rev-parse", "--show-toplevel"],
                check=True,
                capture_output=True,
                text=True,
                cwd=start,
            )
            top = result.stdout.strip()
            if top:
                return Path(top)
        except subprocess.CalledProcessError:
            pass
    return start

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant identifier (GitHub Models uses 'copilot'; leave unset for default)"),
    model: str = typer.Option(None, "--model", help="Specific GitHub Model to use (e.g., gpt-4.1, gpt-4o)"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for VS Code/GitHub Copilot tooling"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
    local: bool = typer.Option(False, "--local", help="Use local templates from development environment (for testing)"),
):
    """
    Initialize a new Specify project from the latest template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Set up your project with GitHub Models integration
    3. Fetch available models and allow selection
    4. Download the appropriate template from GitHub
    5. Extract the template to a new project directory or current directory
    6. Initialize a fresh git repository (if not --no-git and no existing repo)
    7. Set up GitHub Models commands and prompts with model configuration

    Examples:
        specify init my-project                          # Interactive GitHub Model selection
        specify init my-project --model gpt-4o           # Initialize with specific model
        specify init my-project --model gpt-4o --script ps  # Use PowerShell scripts
        specify init my-project --no-git                 # Initialize without git repository
        specify init .                                   # Initialize in current directory
        specify init --here --force                      # Skip confirmation when current directory not empty
    """
    # Show banner first
    show_banner()

    # Handle '.' as shorthand for current directory (equivalent to --here)
    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    # Validate arguments
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)

    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                # Ask for confirmation
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    # Create formatted setup info with column alignment
    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Specify Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    # Add target path only if different from working dir
    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Check git only if we might need it (not --no-git)
    # Only set to True if the user wants it and the tool is available
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", "https://git-scm.com/downloads")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Auto-select when only one assistant is available
        if len(AI_CHOICES) == 1:
            selected_ai = next(iter(AI_CHOICES.keys()))
        else:
            # Use arrow-key selection interface
            selected_ai = select_with_arrows(
                AI_CHOICES,
                "Choose your GitHub Models assistant:",
                "copilot"
            )

    # Model selection (if using GitHub Models)
    selected_model = None
    if selected_ai == "copilot":
        if model:
            # Validate the provided model exists
            console.print(f"[cyan]Validating model '{model}'...[/cyan]")
            available_models = fetch_github_models(github_token)
            if model not in available_models:
                console.print(f"[red]Error:[/red] Model '{model}' not found in GitHub Models catalog.")
                console.print("\n[yellow]Did you mean one of these?[/yellow]")
                # Show similar model names
                similar = [m for m in available_models.keys() if model.lower() in m.lower() or m.lower() in model.lower()]
                if similar:
                    for m in sorted(similar)[:10]:
                        console.print(f"  • {m}")
                else:
                    # Show first 20 models as examples
                    console.print("[yellow]Available models (showing first 20):[/yellow]")
                    for m in sorted(available_models.keys())[:20]:
                        console.print(f"  • {m}")
                console.print(f"\n[dim]Use 'specify list-models' to see all {len(available_models)} available models[/dim]")
                raise typer.Exit(1)
            selected_model = model
            console.print(f"[green]✓[/green] Model '{model}' validated")
        else:
            # Fetch and select from available models (interactive or default)
            console.print("[cyan]Fetching available GitHub Models...[/cyan]")
            available_models = fetch_github_models(github_token)
            if available_models:
                # Check if we're in an interactive terminal
                if sys.stdin.isatty() and sys.stdout.isatty():
                    # Show interactive model selection
                    selected_model = select_with_arrows(
                        available_models,
                        "Choose a GitHub Model:",
                        "gpt-4o" if "gpt-4o" in available_models else list(available_models.keys())[0]
                    )
                else:
                    # Non-interactive: use gpt-4o as default
                    default_model = "gpt-4o" if "gpt-4o" in available_models else list(available_models.keys())[0]
                    selected_model = default_model
                    console.print(f"[dim]Non-interactive mode: using default model '{default_model}'[/dim]")
            else:
                console.print("[yellow]Warning: Could not fetch models from API, using default configuration[/yellow]")
                selected_model = "gpt-4o"  # Fallback default

    # GitHub Models (copilot) doesn't require CLI tools - no checks needed
    # Note: Previously, this section checked for agent CLI tools, but GitHub Copilot
    # integration is built into VS Code and doesn't require external CLI validation.
    # The `ignore_agent_tools` flag is preserved for backwards compatibility.

    # Determine script type (explicit, interactive, or OS default)
    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        # Auto-detect default based on OS
        default_script = "ps" if os.name == "nt" else "sh"
        # Provide interactive selection if in a TTY, otherwise use default
        if sys.stdin.isatty() and sys.stdout.isatty():
            selected_script = select_with_arrows(
                SCRIPT_TYPE_CHOICES,
                "Choose script type (or press Enter for default)",
                default_script
            )
        else:
            selected_script = default_script
            console.print(f"[dim]Non-interactive mode: using default script type '{default_script}'[/dim]")

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    if selected_model:
        console.print(f"[cyan]Selected model:[/cyan] {selected_model}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker("Initialize Specify Project")
    # Flag to allow suppressing legacy headings
    sys._specify_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("workspace", "Sync workspace config"),
        ("chmod", "Ensure scripts executable"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            # Create a httpx client with verify based on skip_tls
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            if local:
                copy_local_template(project_path, selected_ai, selected_script, selected_model, here, verbose=False, tracker=tracker)
            else:
                download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            tracker.start("workspace")
            try:
                synced, detail = sync_workspace_config(project_path, current_dir)
            except Exception as sync_error:
                tracker.error("workspace", str(sync_error))
            else:
                if synced:
                    tracker.complete("workspace", detail)
                else:
                    tracker.skip("workspace", detail)

            # Ensure scripts are executable (POSIX)
            ensure_executable_scripts(project_path, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")

    # Agent folder security notice
    agent_folder_map = {
        "copilot": ".github/"
    }

    if selected_ai in agent_folder_map:
        agent_folder = agent_folder_map[selected_ai]
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    steps_lines.append(f"{step_num}. Start using slash commands with GitHub Models:")

    steps_lines.append("   2.1 [cyan]/constitution[/] - Establish project principles")
    steps_lines.append("   2.2 [cyan]/specify[/] - Create baseline specification")
    steps_lines.append("   2.3 [cyan]/plan[/] - Create implementation plan")
    steps_lines.append("   2.4 [cyan]/tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.5 [cyan]/implement[/] - Execute implementation")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "Optional commands that you can use for your specs [bright_black](improve quality & confidence)[/bright_black]",
        "",
        "○ [cyan]/clarify[/] [bright_black](optional)[/bright_black] - Ask structured questions to de-risk ambiguous areas before planning (run before [cyan]/plan[/] if used)",
        "○ [cyan]/analyze[/] [bright_black](optional)[/bright_black] - Cross-artifact consistency & alignment report (after [cyan]/tasks[/], before [cyan]/implement[/])"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title="Enhancement Commands", border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)



@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    tracker.add("code", "Visual Studio Code")
    tracker.add("code-insiders", "Visual Studio Code Insiders")

    # Add agent checks
    # GitHub Models is IDE-based (no CLI tool required)
    tracker.add("copilot", f"{AI_CHOICES['copilot']} (IDE-based, optional)")

    git_ok = check_tool_for_tracker("git", tracker)
    code_ok = check_tool_for_tracker("code", tracker)
    code_insiders_ok = check_tool_for_tracker("code-insiders", tracker)

    # GitHub Models doesn't need CLI tool check
    tracker.complete("copilot", "IDE-based (no CLI check)")

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")
    if not (code_ok or code_insiders_ok):
        console.print("[dim]Tip: Install VS Code for the best GitHub Models experience[/dim]")


@app.command(name="list-models")
def list_models(
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
    verbose: bool = typer.Option(False, "--verbose", help="Show detailed model information"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip cache and fetch fresh data from API"),
    clear_cache: bool = typer.Option(False, "--clear-cache", help="Clear the models cache and exit")
):
    """List available GitHub Models."""
    show_banner()

    # Handle cache clearing
    if clear_cache:
        cache_file = _models_cache_path()
        if cache_file.exists():
            cache_file.unlink()
            console.print("[green]✓ Models cache cleared[/green]")
        else:
            console.print("[yellow]No cache file found[/yellow]")
        return

    console.print("[bold]Fetching available GitHub Models...[/bold]\n")

    with console.status("[cyan]Contacting GitHub Models API...", spinner="dots"):
        models = fetch_github_models(github_token, use_cache=not no_cache)

    if not models:
        console.print("[red]No models found or API unavailable[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Found {len(models)} available models:[/green]\n")

    # Create a table to display models
    table = Table()
    table.add_column("Model ID", style="cyan", min_width=20)
    table.add_column("Model Name", style="white")

    # Sort models by name for better readability
    sorted_models = sorted(models.items(), key=lambda x: x[1])

    for model_id, model_name in sorted_models:
        table.add_row(model_id, model_name)

    console.print(table)

    if verbose:
        console.print("\n[dim]API endpoint: https://models.inference.ai.azure.com/models[/dim]")
        console.print(f"[dim]Auth: {'✓ Token provided' if _github_token(github_token) else '⚠ No token (may have limited access)'}[/dim]")

    cache_meta = _load_models_cache_metadata()
    if cache_meta:
        age = _format_age(cache_meta.get("age_seconds"))
        source = cache_meta.get("source", "unknown")
        console.print(
            f"\n[dim]Cache: {age} old (source: {source}). Run 'specify list-models --refresh' to force an update.[/dim]"
        )
    elif not no_cache:
        console.print("\n[dim]Cache: none (will populate after the first successful API call).[/dim]")


@app.command()
def status(
    output_json: bool = typer.Option(
        False,
        "--json",
        help="Output status information as JSON instead of formatted text.",
    ),
    agent_mode: bool = typer.Option(
        False,
        "--agent",
        help="Emit a minimal, plain-text summary optimized for automation agents.",
    ),
):
    """
    Show current project configuration and status.

    Displays comprehensive information about:
    - Specify project detection (.specify directory)
    - Workflow artifact completion (constitution, specs, plans, tasks)
    - Feature progress with next-step guidance
    - Configured GitHub Models and prompts
    - Git repository status

    Output Modes:
    - Default: Rich formatted tables and colored output
    - --json: Machine-readable JSON structure
    - --agent: Plain-text format optimized for AI agents

    Examples:
        specify status              # Interactive formatted output
        specify status --json       # JSON for scripting
        specify status --agent      # Agent-friendly plain text
    """

    current_dir = Path.cwd()
    specify_dir = current_dir / ".specify"
    github_dir = current_dir / ".github"
    prompts_dir = github_dir / "prompts"
    config_dir = specify_dir / "config"
    models_config = config_dir / "models.json"

    is_specify_project = specify_dir.exists()

    prompt_files: list[Path] = []
    if prompts_dir.exists():
        prompt_files = sorted(prompts_dir.glob("*.md"))

    config_data: dict | None = None
    config_error: str | None = None
    if models_config.exists():
        try:
            config_data = json.loads(models_config.read_text())
        except Exception as exc:
            config_error = str(exc)

    model_info = None
    scripts_info = None
    if isinstance(config_data, dict):
        github_meta = config_data.get("github_models", {})
        scripts_meta = config_data.get("scripts", {})
        model_info = {
            "selected_model": github_meta.get("selected_model"),
            "last_updated": github_meta.get("last_updated"),
            "catalog_source": github_meta.get("catalog_source"),
            "catalog_cached_at": github_meta.get("catalog_cached_at"),
        }
        scripts_info = {
            "preferred": scripts_meta.get("preferred"),
            "folder": scripts_meta.get("folder"),
            "extension": scripts_meta.get("extension"),
            "last_updated": scripts_meta.get("last_updated"),
        }

    artifact_summary = _collect_workflow_artifacts(specify_dir) if is_specify_project else None
    if artifact_summary is None:
        artifact_summary = {
            "constitution": False,
            "features": [],
            "feature_total": 0,
            "specs_ready": 0,
            "plans_ready": 0,
            "tasks_ready": 0,
            "waiting_plan": [],
            "waiting_tasks": [],
            "missing_spec": [],
        }

    commands = [path.stem for path in prompt_files]
    git_repo = is_git_repo(current_dir)
    cache_meta = _load_models_cache_metadata()
    followups = _derive_followups(artifact_summary)
    primary_suggestion = _pick_primary_suggestion(artifact_summary)

    status_payload = {
        "current_directory": str(current_dir),
        "is_specify_project": is_specify_project,
        "prompts": {
            "configured": bool(prompt_files),
            "count": len(prompt_files),
            "directory": str(prompts_dir),
            "commands": commands,
        },
        "model": model_info,
        "scripts": scripts_info,
        "workflow": artifact_summary,
        "git": {"is_repo": git_repo},
        "models_cache": cache_meta,
        "followups": followups,
        "next_suggestion": primary_suggestion,
        "config_error": config_error,
    }

    if output_json:
        print(json.dumps(status_payload, indent=2))
        return

    if agent_mode:
        # Agent mode: minimal, structured, easy-to-parse output
        if not is_specify_project:
            console.print("ERROR: Not a Specify project (missing .specify directory). Run 'specify init .' first.")
            raise typer.Exit(1)

        # Primary next step (always present)
        next_step_text = primary_suggestion or "All core artifacts ready."
        console.print(f"NEXT_STEP: {next_step_text}")

        # Constitution status
        console.print(
            f"CONSTITUTION: {'ready' if artifact_summary.get('constitution') else 'missing'}"
        )

        # Feature breakdown
        if artifact_summary["features"]:
            console.print("FEATURES:")
            for feature in artifact_summary["features"]:
                console.print(
                    "- {slug}: spec={spec} plan={plan} tasks={tasks} next={next_cmd}".format(
                        slug=feature.get("slug", "unknown"),
                        spec="done" if feature.get("spec") else "todo",
                        plan="done" if feature.get("plan") else "todo",
                        tasks="done" if feature.get("tasks") else "todo",
                        next_cmd=feature.get("next_command", "unknown"),
                    )
                )
        else:
            console.print("FEATURES: none (run /specify to create one)")

        # Available commands
        if commands:
            console.print(
                "COMMANDS: " + ", ".join(f"/{name}" for name in commands[:10]) + (
                    " …" if len(commands) > 10 else ""
                )
            )

        # Additional followup suggestions
        if followups:
            console.print("FOLLOWUPS:")
            for item in followups[:5]:
                console.print(f"- {item}")

        return

    show_banner()

    console.print("[bold]Project Status[/bold]\n")
    console.print(f"[cyan]Current Directory:[/cyan] {current_dir}")

    if not is_specify_project:
        console.print("[red]⚠ Not a Specify project[/red] (no .specify directory found)")
        console.print("[dim]Run 'specify init .' to initialize this directory as a Specify project[/dim]")
        return

    console.print("[green]✓ Specify project detected[/green]")

    if primary_suggestion:
        console.print(f"[bold magenta]Next step:[/bold magenta] {primary_suggestion}")

    if prompt_files:
        console.print(f"[cyan]AI Assistant:[/cyan] GitHub Models ({len(prompt_files)} prompts configured)")
    else:
        console.print("[yellow]⚠ No GitHub Models prompts found[/yellow]")

    github_meta = model_info or {}
    selected_model = github_meta.get("selected_model") if github_meta else None
    last_updated_raw = github_meta.get("last_updated") if github_meta else None
    catalog_source = github_meta.get("catalog_source") if github_meta else None
    catalog_cached_at = github_meta.get("catalog_cached_at") if github_meta else None

    if config_error and models_config.exists():
        console.print("[yellow]⚠ Model configuration file exists but could not be read[/yellow]")
    elif selected_model:
        last_updated_dt = _parse_iso8601(last_updated_raw)
        if last_updated_dt:
            age = _format_age((datetime.now(timezone.utc) - last_updated_dt).total_seconds())
            iso_stamp = last_updated_dt.isoformat().replace("+00:00", "Z")
            console.print(
                f"[cyan]Selected Model:[/cyan] {selected_model} [dim](set {age} ago · {iso_stamp})[/dim]"
            )
        else:
            console.print(
                f"[cyan]Selected Model:[/cyan] {selected_model} [dim](configured {last_updated_raw or 'unknown'})[/dim]"
            )
    else:
        console.print("[dim]No specific model configured (will use default)[/dim]")

    if catalog_source:
        console.print(f"[dim]Catalog source: {catalog_source}[/dim]")

    if catalog_cached_at:
        cached_dt = _parse_iso8601(catalog_cached_at)
        if cached_dt:
            cache_age = _format_age((datetime.now(timezone.utc) - cached_dt).total_seconds())
            console.print(
                f"[dim]Catalog cached: {cache_age} ago ({cached_dt.isoformat().replace('+00:00', 'Z')})[/dim]"
            )

    scripts_meta = scripts_info or {}
    if scripts_meta:
        script_flavor = scripts_meta.get("preferred", "unknown")
        descriptor = "/".join(filter(None, [scripts_meta.get("folder"), scripts_meta.get("extension")]))
        last_script_dt = _parse_iso8601(scripts_meta.get("last_updated"))
        if last_script_dt:
            script_age = _format_age((datetime.now(timezone.utc) - last_script_dt).total_seconds())
            console.print(
                f"[cyan]Script Flavor:[/cyan] {script_flavor} [dim]({descriptor or 'n/a'}, updated {script_age} ago)[/dim]"
            )
        else:
            console.print(f"[cyan]Script Flavor:[/cyan] {script_flavor} [dim]({descriptor or 'n/a'})[/dim]")

    _render_workflow_summary(artifact_summary)
    _render_feature_details(artifact_summary)

    if git_repo:
        console.print("[green]✓ Git repository initialized[/green]")
    else:
        console.print("[dim]No git repository (use 'git init' to initialize)[/dim]")

    if prompt_files:
        console.print(f"\n[bold]Available Commands ({len(prompt_files)}):[/bold]")
        for name in commands:
            console.print(f"  [cyan]/{name}[/cyan]")

    if cache_meta:
        age_human = _format_age(cache_meta.get("age_seconds"))
        source = cache_meta.get("source", "unknown")
        console.print(
            f"\n[dim]Models cache: {age_human} old (source: {source}). Use 'specify list-models --refresh' to update.[/dim]"
        )
    else:
        console.print(
            "\n[dim]Models cache: none (will populate after the first successful API call).[/dim]"
        )


@app.command()
def version():
    """Show version information."""
    show_banner()

    # Try to get version from package metadata
    try:
        import importlib.metadata
        pkg_version = importlib.metadata.version("specify-cli")
    except Exception:
        # Fallback version if package not installed
        pkg_version = "development"

    console.print(f"[bold]Specify CLI Version:[/bold] {pkg_version}")
    console.print(f"[cyan]Python:[/cyan] {sys.version.split()[0]}")
    console.print(f"[cyan]Platform:[/cyan] {sys.platform}")

    # Show cache info if available
    cache_file = Path.home() / ".specify" / "models_cache.json"
    if cache_file.exists():
        import time
        cache_stat = cache_file.stat()
        cache_age = time.time() - cache_stat.st_mtime
        if cache_age < 3600:
            console.print(f"[dim]Models cache: ✓ (fresh, {int(cache_age/60)} minutes old)[/dim]")
        else:
            console.print(f"[dim]Models cache: ⚠ (stale, {int(cache_age/3600)} hours old)[/dim]")
    else:
        console.print("[dim]Models cache: none[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
