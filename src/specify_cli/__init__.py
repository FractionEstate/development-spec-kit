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
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from datetime import datetime
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
    cache_file = Path.home() / ".specify" / "models_cache.json"

    # Check cache first (if enabled and recent)
    if use_cache and cache_file.exists():
        try:
            cache_stat = cache_file.stat()
            # Use cache if less than 1 hour old
            import time
            if time.time() - cache_stat.st_mtime < 3600:  # 1 hour
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    if cached_data.get("models"):
                        return cached_data["models"]
        except Exception:
            pass  # Ignore cache errors, continue with API fetch

    try:
        with httpx.Client(verify=ssl_context, timeout=10.0) as client:
            # Try the GitHub Models marketplace API first
            try:
                response = client.get(
                    "https://api.github.com/marketplace_listing/plans",
                    headers=_github_auth_headers(github_token)
                )
                if response.status_code == 200:
                    # This would be for GitHub Marketplace, but models are likely different API
                    pass
            except Exception:
                pass

            # Try Azure AI Models API
            response = client.get(
                "https://models.inference.ai.azure.com/models",
                headers=_github_auth_headers(github_token)
            )
            if response.status_code == 200:
                models_data = response.json()

                # Combine API results with known GitHub Models
                api_models = {}

                # Parse the models response and create a clean mapping
                if isinstance(models_data, dict) and "data" in models_data:
                    for model in models_data["data"]:
                        model_id = model.get("id", "")
                        model_name = model.get("name", model_id)
                        if model_id:
                            # Simplify model IDs for better usability
                            simple_id = model_id.split("/")[-2] if "/" in model_id else model_id
                            api_models[simple_id] = model_name
                elif isinstance(models_data, list):
                    # Handle direct list format
                    for model in models_data:
                        model_id = model.get("id", "")
                        model_name = model.get("name", model_id)
                        if model_id:
                            simple_id = model_id.split("/")[-2] if "/" in model_id else model_id
                            api_models[simple_id] = model_name

                # Merge with fallback known models (fallback takes precedence for known models)
                fallback_models = get_fallback_github_models()
                combined_models = {**api_models, **fallback_models}

                # Save to cache for future use
                if use_cache:
                    try:
                        cache_file.parent.mkdir(parents=True, exist_ok=True)
                        import time
                        cache_data = {
                            "models": combined_models,
                            "timestamp": time.time(),
                            "source": "api_with_fallback"
                        }
                        with open(cache_file, 'w') as f:
                            json.dump(cache_data, f, indent=2)
                    except Exception:
                        pass  # Ignore cache save errors

                return combined_models
            else:
                # Fallback to known models if API fails
                return get_fallback_github_models()
    except Exception:
        # Fallback to known models if any error occurs
        return get_fallback_github_models()

def get_fallback_github_models() -> dict:
    """Return a fallback list of known GitHub Models when API is unavailable."""
    return {
        "gpt-4": "GPT-4",
        "gpt-4-turbo": "GPT-4 Turbo",
        "gpt-4.1": "GPT-4.1",
        "gpt-4o": "GPT-4o",
        "gpt-4o-mini": "GPT-4o Mini",
        "gpt-5-mini": "GPT-5 Mini",
        "gpt-5": "GPT-5",
        "gpt-5-codex": "GPT-5 Codex",
        "grok-code-fast-1": "Grok Code Fast 1",
        "claude-3-5-sonnet": "Claude Sonnet 3.5",
        "claude-3-7-sonnet": "Claude Sonnet 3.7",
        "claude-4-sonnet": "Claude Sonnet 4",
        "gemini-2.5-pro": "Gemini 2.5 Pro",
        "o3-mini": "o3-mini",
        "o4-mini": "o4-mini",
        # Additional models from Azure/GitHub Models marketplace
        "meta-llama-3-70b-instruct": "Meta Llama 3 70B Instruct",
        "meta-llama-3-8b-instruct": "Meta Llama 3 8B Instruct",
        "meta-llama-3.1-405b-instruct": "Meta Llama 3.1 405B Instruct",
        "meta-llama-3.1-70b-instruct": "Meta Llama 3.1 70B Instruct",
        "meta-llama-3.1-8b-instruct": "Meta Llama 3.1 8B Instruct",
        "mistral-nemo": "Mistral Nemo",
        "mistral-large-2407": "Mistral Large 2407",
        "mistral-small": "Mistral Small",
        "ai21-jamba-instruct": "AI21 Jamba Instruct",
        "cohere-embed-v3-english": "Cohere Embed v3 English",
        "cohere-embed-v3-multilingual": "Cohere Embed v3 Multilingual"
    }

# Constants
AI_CHOICES = {
    "copilot": "GitHub Models",
}
# Add script type choices
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

# Agent configurations for setup (directory, format, arg placeholder)
agent_configs = {
    "copilot": {"dir": ".github/prompts", "format": "md", "arg_placeholder": "$ARGUMENTS"},
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
            except Exception:
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

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
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


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
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
        subprocess.run(
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
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True

    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "FractionEstate"
    repo_name = "development-spec-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
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
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
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
        console.print(f"[cyan]Downloading template...[/cyan]")

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
        console.print(f"[red]Error downloading template[/red]")
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

        # Copy all template files to project root
        for item in dev_templates_dir.iterdir():
            if item.name.startswith('.'):
                continue  # Skip hidden files like .github, .vscode
            dest = project_path / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

        # Create .specify directory and copy development files
        specify_dir = project_path / ".specify"
        specify_dir.mkdir(exist_ok=True)

        # Copy memory
        if dev_memory_dir.exists():
            shutil.copytree(dev_memory_dir, specify_dir / "memory", dirs_exist_ok=True)

        # Copy scripts
        if dev_scripts_dir.exists():
            shutil.copytree(dev_scripts_dir, specify_dir / "scripts", dirs_exist_ok=True)

        # Copy templates to .specify/templates
        shutil.copytree(dev_templates_dir, specify_dir / "templates", dirs_exist_ok=True)

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

    # Store model configuration if provided
    if selected_model and ai_assistant == "copilot":
        config_dir = project_path / ".specify" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_data = {
            "github_models": {
                "selected_model": selected_model,
                "last_updated": datetime.utcnow().isoformat()
            }
        }

        config_file = config_dir / "models.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    # Process each command template
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.md"):
            command_name = template_file.stem
            content = template_file.read_text()

            # Replace placeholders
            content = content.replace("$ARGUMENTS", config["arg_placeholder"])
            content = content.replace("{SCRIPT}", f".specify/scripts/{script_type}/{template_file.stem}.{script_type}")

            if config["format"] == "toml":
                # Wrap in TOML format
                description = content.split('\n', 1)[0].strip('# ').strip()  # Extract description from first line
                prompt_content = content.replace(f'# {description}', '', 1).strip()
                content = f'description = "{description}"\n\nprompt = """\n{prompt_content}\n"""'
                output_file = output_dir / f"{command_name}.toml"
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
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

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
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
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
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

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
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
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

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant identifier (GitHub Models uses 'copilot'; leave unset for default)"),
    model: str = typer.Option(None, "--model", help="Specific GitHub Model to use (e.g., gpt-4o, claude-3-5-sonnet)"),
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
            available_models = fetch_github_models(github_token)
            if model not in available_models:
                console.print(f"[red]Error:[/red] Model '{model}' not found.")
                console.print(f"[yellow]Available models:[/yellow] {', '.join(sorted(available_models.keys()))}")
                console.print(f"[dim]Use 'specify list-models' to see all available models[/dim]")
                raise typer.Exit(1)
            selected_model = model
        else:
            # Fetch and select from available models
            console.print("[cyan]Fetching available GitHub Models...[/cyan]")
            available_models = fetch_github_models(github_token)
            if available_models:
                # Show interactive model selection
                selected_model = select_with_arrows(
                    available_models,
                    "Choose a GitHub Model:",
                    "gpt-4o" if "gpt-4o" in available_models else list(available_models.keys())[0]
                )
            else:
                console.print("[yellow]Warning: Could not fetch models from API, using default configuration[/yellow]")

    # GitHub Models (copilot) doesn't require CLI tools - no checks needed
    if not ignore_agent_tools:
        agent_tool_missing = False

        if agent_tool_missing:
            error_panel = Panel(
                f"[cyan]{selected_ai}[/cyan] not found\n"
                f"Install with: [cyan]{install_url}[/cyan]\n"
                f"{AI_CHOICES[selected_ai]} is required to continue with this project type.\n\n"
                "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                title="[red]Agent Detection Error[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    # Determine script type (explicit, interactive, or OS default)
    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        # Auto-detect default
        default_script = "ps" if os.name == "nt" else "sh"
        # Provide interactive selection similar to AI if stdin is a TTY
        if sys.stdin.isatty():
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        else:
            selected_script = default_script

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
        f"○ [cyan]/clarify[/] [bright_black](optional)[/bright_black] - Ask structured questions to de-risk ambiguous areas before planning (run before [cyan]/plan[/] if used)",
        f"○ [cyan]/analyze[/] [bright_black](optional)[/bright_black] - Cross-artifact consistency & alignment report (after [cyan]/tasks[/], before [cyan]/implement[/])"
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
        cache_file = Path.home() / ".specify" / "models_cache.json"
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
        console.print(f"\n[dim]API endpoint: https://models.inference.ai.azure.com/models[/dim]")
        console.print(f"[dim]Auth: {'✓ Token provided' if _github_token(github_token) else '⚠ No token (may have limited access)'}[/dim]")


@app.command()
def status():
    """Show current project configuration and status."""
    show_banner()

    current_dir = Path.cwd()
    console.print(f"[bold]Project Status[/bold]\n")
    console.print(f"[cyan]Current Directory:[/cyan] {current_dir}")

    # Check if this is a Specify project
    specify_dir = current_dir / ".specify"
    github_dir = current_dir / ".github"
    prompts_dir = github_dir / "prompts"
    config_dir = specify_dir / "config"
    models_config = config_dir / "models.json"

    if not specify_dir.exists():
        console.print("[red]⚠ Not a Specify project[/red] (no .specify directory found)")
        console.print("[dim]Run 'specify init .' to initialize this directory as a Specify project[/dim]")
        return

    console.print("[green]✓ Specify project detected[/green]")

    # Show AI configuration
    if prompts_dir.exists():
        prompt_files = list(prompts_dir.glob("*.md"))
        console.print(f"[cyan]AI Assistant:[/cyan] GitHub Models ({len(prompt_files)} prompts configured)")

        # Show selected model if configured
        if models_config.exists():
            try:
                with open(models_config, 'r') as f:
                    config_data = json.load(f)
                selected_model = config_data.get("github_models", {}).get("selected_model")
                last_updated = config_data.get("github_models", {}).get("last_updated", "unknown")
                if selected_model:
                    console.print(f"[cyan]Selected Model:[/cyan] {selected_model} [dim](configured {last_updated})[/dim]")
            except Exception:
                console.print("[yellow]⚠ Model configuration file exists but could not be read[/yellow]")
        else:
            console.print("[dim]No specific model configured (will use default)[/dim]")
    else:
        console.print("[yellow]⚠ No GitHub Models prompts found[/yellow]")

    # Check for git repository
    if is_git_repo(current_dir):
        console.print("[green]✓ Git repository initialized[/green]")
    else:
        console.print("[dim]No git repository (use 'git init' to initialize)[/dim]")

    # Show available commands
    if prompts_dir.exists():
        prompt_files = sorted(prompts_dir.glob("*.md"))
        if prompt_files:
            console.print(f"\n[bold]Available Commands ({len(prompt_files)}):[/bold]")
            for prompt_file in prompt_files:
                command_name = prompt_file.stem
                console.print(f"  [cyan]/{command_name}[/cyan]")


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
        console.print(f"[dim]Models cache: none[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
