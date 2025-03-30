"""
Main entry point for the Gemini CLI application.
Targets Gemini 2.5 Pro Experimental. Includes ASCII Art welcome.
"""

import os
import sys
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from pathlib import Path
import yaml
import google.generativeai as genai
import logging
import time # Added for potential small delay

# Import the updated model class and listing function
from .models.gemini import GeminiModel, list_available_models
from .config import Config
from .utils import count_tokens

# Setup console and config
console = Console()
try:
    config = Config()
except Exception as e:
    console.print(f"[bold red]Error loading configuration:[/bold red] {e}")
    config = None

# Setup logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
log = logging.getLogger(__name__)

# --- Default Model ---
# Keep targeting 2.5 Pro as requested
DEFAULT_MODEL = "gemini-2.5-pro-exp-03-25"
# --- ---

# --- ASCII Art Definition ---
GEMINI_CODE_ART = r"""

[medium_purple]
  ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗        ██████╗  ██████╗ ██████╗ ███████╗
 ██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║       ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝
 ██║ ███╗███████╗██╔████╔██║██║██╔██╗ ██║██║       ██║      ██║   ██║██║  ██║███████╗
 ██║  ██║██╔════╝██║╚██╔╝██║██║██║╚██╗██║██║       ██║      ██║   ██║██║  ██║██╔════╝
 ╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║       ╚██████╗ ╚██████╔╝██████╔╝███████╗
  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝        ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝
[/medium_purple]
"""
# --- End ASCII Art ---


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    '--model', '-m',
    help=f'Model ID to use (e.g., gemini-2.5-pro-exp-03-25). Default: {DEFAULT_MODEL}',
    default=None
)
@click.pass_context
def cli(ctx, model):
    """Interactive CLI for Gemini models with coding assistance tools."""
    if not config:
        console.print("[bold red]Configuration could not be loaded. Cannot proceed.[/bold red]")
        sys.exit(1)

    if ctx.invoked_subcommand is None:
        model_name_to_use = model or config.get_default_model() or DEFAULT_MODEL
        log.info(f"Attempting to start interactive session with model: {model_name_to_use}")
        start_interactive_session(model_name_to_use)

# ... (setup, set_default_model, list_models functions remain the same) ...
@cli.command()
@click.argument('key', required=True)
def setup(key):
    """Set and save your Google Generative AI API key."""
    if not config: console.print("[bold red]Config error.[/bold red]"); return
    try: config.set_api_key("google", key); console.print("[green]✓[/green] Google API key saved.")
    except Exception as e: console.print(f"[bold red]Error saving API key:[/bold red] {e}")

@cli.command()
@click.argument('model_name', required=True)
def set_default_model(model_name):
    """Set the default Gemini model to use."""
    if not config: console.print("[bold red]Config error.[/bold red]"); return
    try: config.set_default_model(model_name); console.print(f"[green]✓[/green] Default model set to [bold]{model_name}[/bold].")
    except Exception as e: console.print(f"[bold red]Error setting default model:[/bold red] {e}")

@cli.command()
def list_models():
    """List available models accessible with your API key."""
    if not config: console.print("[bold red]Config error.[/bold red]"); return
    api_key = config.get_api_key("google")
    if not api_key: console.print("[bold red]Error:[/bold red] API key not found. Run 'gemini setup'."); return
    console.print("[yellow]Fetching models...[/yellow]")
    try:
        models_list = list_available_models(api_key)
        if not models_list or (isinstance(models_list, list) and len(models_list) > 0 and isinstance(models_list[0], dict) and "error" in models_list[0]):
             console.print(f"[red]Error listing models:[/red] {models_list[0].get('error', 'Unknown error') if models_list else 'No models found or fetch error.'}"); return
        console.print("\n[bold cyan]Available Models (Access may vary):[/bold cyan]")
        for model_data in models_list: console.print(f"- [bold green]{model_data['name']}[/bold green] (Display: {model_data.get('display_name', 'N/A')})")
        console.print("\nUse 'gemini --model MODEL' or 'gemini set-default-model MODEL'.")
    except Exception as e: console.print(f"[bold red]Error listing models:[/bold red] {e}"); log.error("List models failed", exc_info=True)


def start_interactive_session(model_name):
    """Start an interactive chat session with the selected Gemini model."""
    if not config: console.print("[bold red]Config error.[/bold red]"); return

    # --- Display Welcome Art ---
    console.clear() # Optional: Clear screen before showing art
    console.print(GEMINI_CODE_ART)
    console.print(Panel("[b]Welcome to Gemini Code AI Assistant![/b]", border_style="blue", expand=False))
    time.sleep(0.1) # Small pause can sometimes help rendering
    # --- End Welcome Art ---

    api_key = config.get_api_key("google")
    if not api_key:
        console.print("\n[bold red]Error:[/bold red] Google API key not found.")
        console.print("Please run [bold]'gemini setup YOUR_API_KEY'[/bold] first.")
        return

    try:
        # Show model initialization message *after* the art
        console.print(f"\nInitializing model [bold]{model_name}[/bold]...")
        model = GeminiModel(api_key=api_key, model_name=model_name)
        console.print("[green]Model initialized successfully.[/green]\n")

    except Exception as e:
        console.print(f"\n[bold red]Error initializing model '{model_name}':[/bold red] {e}")
        log.error(f"Failed to initialize model {model_name}", exc_info=True)
        console.print("Please check model name, API key permissions, network. Use 'gemini list-models'.")
        return

    # --- Session Start Message ---
    console.print("Type '/help' for commands, '/exit' or Ctrl+C to quit.")

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")

            if user_input.lower() == '/exit': break
            elif user_input.lower() == '/help': show_help(); continue

            with console.status("[yellow]Assistant thinking...", spinner="dots"):
                response_text = model.generate(user_input)

            if response_text is None and user_input.startswith('/'): console.print(f"[yellow]Unknown command:[/yellow] {user_input}"); continue
            elif response_text is None: console.print("[red]Empty response received.[/red]"); log.warning("generate() returned None."); continue

            console.print("[bold green]Assistant:[/bold green]")
            console.print(Markdown(response_text), highlight=True) # Added highlight=True for code

        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted. Exiting.[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred during the session:[/bold red] {e}")
            log.error("Error during interactive loop", exc_info=True)


def show_help():
    """Show help information for interactive mode."""
    # ... (show_help function remains the same) ...
    tool_names = list(AVAILABLE_TOOLS.keys()) if AVAILABLE_TOOLS else ["None"]
    help_text = f""" [bold]Help[/bold]\n [cyan]Commands:[/cyan]\n  /exit, /help\n [cyan]CLI:[/cyan]\n  gemini setup KEY\n  gemini list-models\n  gemini set-default-model NAME\n  gemini --model NAME\n [cyan]Workflow:[/cyan] Analyze->Gather Info(tools)->Plan->Execute(tools)->Verify(tools)->Summarize\n [cyan]Tools:[/cyan] {', '.join(tool_names)} """
    console.print(Panel(Markdown(help_text), title="Help", border_style="green"))


if __name__ == "__main__":
    cli()