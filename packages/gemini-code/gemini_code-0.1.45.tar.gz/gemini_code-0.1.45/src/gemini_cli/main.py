"""
Main entry point for the Gemini CLI application.
Targets Gemini 2.5 Pro Experimental.
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

from .models.gemini import GeminiModel, list_available_models
from .config import Config
from .utils import count_tokens

console = Console()
try:
    config = Config()
except Exception as e:
    console.print(f"[bold red]Error loading configuration:[/bold red] {e}")
    config = None

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
log = logging.getLogger(__name__)

# --- Default Model (Updated) ---
DEFAULT_MODEL = "gemini-2.5-pro-exp-03-25" # <-- Specific 2.5 Pro identifier
# --- ---

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    '--model', '-m',
    # --- Updated Help Text ---
    help=f'Model ID to use (e.g., gemini-2.5-pro-exp-03-25, gemini-1.5-pro-latest). Default: {DEFAULT_MODEL}',
    # --- ---
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

@cli.command()
@click.argument('key', required=True)
def setup(key):
    """Set and save your Google Generative AI API key."""
    # ... (setup function remains the same) ...
    if not config:
        console.print("[bold red]Configuration system error.[/bold red]")
        return
    try:
        if not key or len(key) < 30:
             console.print("[bold yellow]Warning:[/bold yellow] API key seems short, but saving anyway.")
        config.set_api_key("google", key)
        console.print("[green]✓[/green] Google API key saved successfully.")
        console.print("You can now start the interactive session using: `gemini`")
    except Exception as e:
        console.print(f"[bold red]Error saving API key:[/bold red] {e}")

@cli.command()
@click.argument('model_name', required=True)
def set_default_model(model_name):
    """Set the default Gemini model to use."""
    # ... (set_default_model function remains the same) ...
    if not config:
        console.print("[bold red]Configuration system error.[/bold red]")
        return
    try:
        config.set_default_model(model_name)
        console.print(f"[green]✓[/green] Default model set to [bold]{model_name}[/bold].")
    except Exception as e:
        console.print(f"[bold red]Error setting default model:[/bold red] {e}")


@cli.command()
def list_models():
    """List available models accessible with your API key."""
    # ... (list_models function remains the same) ...
    if not config:
        console.print("[bold red]Configuration system error.[/bold red]")
        return

    api_key = config.get_api_key("google")
    if not api_key:
        console.print("[bold red]Error:[/bold red] Google API key not found.")
        console.print("Please run [bold]'gemini setup YOUR_API_KEY'[/bold] first.")
        return

    console.print("[yellow]Fetching available models...[/yellow]")
    try:
        models_list = list_available_models(api_key)

        if not models_list:
            console.print("[red]No models found or an error occurred while fetching.[/red]")
            return

        if isinstance(models_list, list) and len(models_list) > 0 and isinstance(models_list[0], dict) and "error" in models_list[0]:
             console.print(f"[red]Error listing models:[/red] {models_list[0]['error']}")
             return

        console.print("\n[bold cyan]Available Models (Access may vary):[/bold cyan]")

        for model_data in models_list:
            display_name = model_data.get('display_name', 'N/A')
            console.print(f"- [bold green]{model_data['name']}[/bold green] (Display: {display_name})")

        console.print("\nUse [bold]'gemini --model MODEL_NAME'[/bold] to start a session with a specific model.")
        console.print("Use [bold]'gemini set-default-model MODEL_NAME'[/bold] to set your preferred default.")

    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred while listing models:[/bold red] {e}")
        log.error("Failed to list models", exc_info=True)

def start_interactive_session(model_name):
    """Start an interactive chat session with the selected Gemini model."""
    # ... (start_interactive_session function remains the same, relies on GeminiModel init) ...
    if not config:
        console.print("[bold red]Configuration system error.[/bold red]")
        return

    api_key = config.get_api_key("google")
    if not api_key:
        console.print("[bold red]Error:[/bold red] Google API key not found.")
        console.print("Please run [bold]'gemini setup YOUR_API_KEY'[/bold] first.")
        return

    try:
        console.print(f"Initializing model [bold]{model_name}[/bold]...")
        model = GeminiModel(api_key=api_key, model_name=model_name)
        console.print("[green]Model initialized successfully.[/green]")

    except Exception as e:
        console.print(f"[bold red]Error initializing model '{model_name}':[/bold red] {e}")
        log.error(f"Failed to initialize model {model_name}", exc_info=True)
        # Add hint about experimental access
        console.print("Please check the model name, your API key permissions (especially for experimental models), and network connection.")
        console.print("Use [bold]'gemini list-models'[/bold] to see available models.")
        return

    console.print(Panel(f"[bold]Gemini Code[/bold] - Using model: [cyan]{model.model_name}[/cyan]", border_style="blue"))
    console.print("Type '/help' for commands, '/exit' or Ctrl+C to quit.")

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")

            if user_input.lower() == '/exit': break
            elif user_input.lower() == '/help': show_help(); continue

            with console.status("[yellow]Assistant thinking...", spinner="dots"):
                response_text = model.generate(user_input)

            if response_text is None and user_input.startswith('/'):
                console.print(f"[yellow]Unknown command:[/yellow] {user_input}")
                continue
            elif response_text is None:
                 console.print("[red]Received an empty response from the model.[/red]")
                 log.warning("Model generate() returned None unexpectedly.")
                 continue

            console.print("[bold green]Assistant:[/bold green]")
            console.print(Markdown(response_text))

        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted. Exiting.[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred during the session:[/bold red] {e}")
            log.error("Error during interactive loop", exc_info=True)


def show_help():
    """Show help information for interactive mode."""
    # ... (show_help function remains largely the same, update tool list if needed) ...
    # Get list of tools dynamically for help text
    tool_names = list(AVAILABLE_TOOLS.keys()) if AVAILABLE_TOOLS else ["None"]
    help_text = f"""
[bold]Gemini Code Assistant Help[/bold]

[cyan]Interactive Commands:[/cyan]
  /exit       Exit the chat session.
  /help       Show this help message.

[cyan]CLI Commands (Run outside chat):[/cyan]
  gemini setup YOUR_API_KEY   Set your Google API key.
  gemini list-models          List available models.
  gemini set-default-model MODEL_NAME Set the default model.
  gemini --model MODEL_NAME   Start a session with a specific model.

[cyan]How it Works:[/cyan]
Type coding requests. The assistant uses tools to interact with your files
and environment. It aims to: Analyze -> Gather Info (using tools) ->
Plan -> Execute (using tools) -> Verify (using tools) -> Summarize.

[cyan]Available Tools:[/cyan] {', '.join(tool_names)}
"""
    console.print(Panel(Markdown(help_text), title="Help", border_style="green"))


if __name__ == "__main__":
    cli()