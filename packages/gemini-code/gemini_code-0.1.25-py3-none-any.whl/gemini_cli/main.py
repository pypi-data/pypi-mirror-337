"""
Main entry point for the Gemini CLI application.
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

from .models.gemini import GeminiModel, list_available_models
from .config import Config
from .utils import count_tokens

console = Console()
config = Config()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('--model', '-m', help='Model to use (default: gemini-2.5-pro)')
@click.pass_context
def cli(ctx, model):
    """Interactive CLI for Gemini and other LLM models."""
    if ctx.invoked_subcommand is None:
        # If no subcommand is specified, start interactive session
        model_name = model or config.get_default_model() or "gemini-2.5-pro"
        start_interactive_session(model_name)

@cli.command()
@click.argument('key')
def setup(key):
    """Set up your Google API key."""
    config.set_api_key("google", key)
    console.print("[green]✓[/green] Google API key saved successfully.")

@cli.command()
@click.argument('model_name')
def set_default_model(model_name):
    """Set the default model to use."""
    config.set_default_model(model_name)
    console.print(f"[green]✓[/green] Default model set to {model_name}.")

@cli.command()
def list_models():
    """List all available Gemini models."""
    api_key = config.get_api_key("google")
    if not api_key:
        console.print("[red]Error:[/red] Google API key not found. Please run 'gemini setup YOUR_API_KEY' first.")
        return
    
    console.print("[yellow]Fetching available models...[/yellow]")
    models = list_available_models(api_key)
    
    if not models:
        console.print("[red]No models found or an error occurred.[/red]")
        return
    
    if "error" in models[0]:
        console.print(f"[red]Error listing models:[/red] {models[0]['error']}")
        return
    
    console.print("\n[bold]Available Gemini Models:[/bold]")
    
    for model in models:
        # Create a formatted panel for each model
        model_content = f"[bold]{model['name']}[/bold]\n"
        if model.get('display_name'):
            model_content += f"Display Name: {model['display_name']}\n"
        if model.get('description'):
            model_content += f"Description: {model['description']}\n"
        if model.get('supported_generation_methods'):
            model_content += f"Supported Methods: {', '.join(model['supported_generation_methods'])}"
        
        console.print(Panel(model_content, title=model["name"], border_style="green"))
    
    console.print("\nTo use a specific model: [bold]gemini --model MODEL_NAME[/bold]")
    console.print("To set the default model: [bold]gemini set-default-model MODEL_NAME[/bold]")

def start_interactive_session(model_name):
    """Start an interactive chat session with the model."""
    # Initialize model based on name
    if model_name.startswith("gemini"):
        api_key = config.get_api_key("google")
        if not api_key:
            console.print("[red]Error:[/red] Google API key not found. Please run 'gemini setup YOUR_API_KEY' first.")
            return
        
        try:
            # Configure the API with the provided key
            genai.configure(api_key=api_key)
            
            # Test the model with a simple generation to verify it works
            try:
                # Create a simpler test without tools to verify basic connectivity
                test_model = genai.GenerativeModel(model_name)
                test_model.generate_content("Hello")
            except Exception as e:
                if "404" in str(e) or "not found" in str(e).lower():
                    console.print(f"[red]Error:[/red] Model '{model_name}' not found. Use 'gemini list-models' to see available models.")
                    return
                elif "403" in str(e) or "permission" in str(e).lower():
                    console.print(f"[red]Error:[/red] You don't have permission to use model '{model_name}'.")
                    return
                else:
                    # For other errors, continue anyway as it might be a temporary issue
                    console.print(f"[yellow]Warning:[/yellow] {str(e)}")
            
            # If the test succeeded, create the actual model with tools
            model = GeminiModel(api_key, model_name)
        except Exception as e:
            console.print(f"[red]Error initializing model:[/red] {str(e)}")
            console.print("[yellow]Tip:[/yellow] Run 'gemini list-models' to see available models.")
            return
    else:
        console.print(f"[red]Error:[/red] Model {model_name} not supported yet.")
        return

    # Session state
    conversation = []
    token_count = 0
    
    # Get thresholds from config
    token_warning_threshold = config.get_setting("token_warning_threshold", 800000)  # 80% of 1M for Gemini
    auto_compact_threshold = config.get_setting("auto_compact_threshold", 950000)  # 95% of 1M

    console.print(Panel(f"[bold]Gemini Code[/bold] - Using model: {model_name}"))
    console.print("Type '/help' for commands, '/exit' to quit.")
    
    while True:
        try:
            # Get user input
            user_input = console.input("[bold blue]You:[/bold blue] ")
            
            # Handle special commands
            if user_input.lower() == '/exit':
                break
            elif user_input.lower() == '/help':
                show_help()
                continue
            elif user_input.lower() == '/compact':
                console.print("[yellow]Compacting conversation...[/yellow]")
                # Request summary from model
                summary_prompt = "Create a detailed summary of our conversation so far that captures all important context, code snippets, and decisions made. This will be used as context for continuing our conversation."
                summary = model.generate(summary_prompt, conversation)
                # Reset conversation with summary
                conversation = [
                    {"role": "system", "content": "The following is a summary of the conversation so far: " + summary},
                    {"role": "system", "content": "Continue the conversation based on this summary."}
                ]
                token_count = count_tokens(str(conversation))
                console.print(f"[green]Conversation compacted. New token count: {token_count}[/green]")
                continue
            
            # Add user message to conversation
            conversation.append({"role": "user", "content": user_input})
            
            # Generate response
            response = model.generate(user_input, conversation)
            
            # If it's a special command, response might be None (handled by the main loop)
            if response is None:
                continue
                
            # Add response to conversation
            conversation.append({"role": "assistant", "content": response})
            
            # Display the response
            console.print("[bold green]Assistant:[/bold green]")
            console.print(Markdown(response))
            
            # Update token count
            token_count = count_tokens(str(conversation))
            
            # Warn if approaching token limit
            if token_count > token_warning_threshold:
                warning_message = f"Warning: Approaching token limit ({token_count}/{token_warning_threshold}). Consider using /compact to summarize the conversation."
                console.print(Panel(warning_message, title="Context Limit Warning", border_style="yellow"))
                
                # If very close to limit (95%), suggest auto-compacting
                if token_count > auto_compact_threshold:
                    console.print("[bold yellow]Would you like to compact the conversation now? (y/n)[/bold yellow]")
                    response = console.input()
                    if response.lower() in ['y', 'yes']:
                        console.print("[yellow]Compacting conversation...[/yellow]")
                        # Request summary from model
                        summary_prompt = "Create a detailed summary of our conversation so far that captures all important context, code snippets, and decisions made. This will be used as context for continuing our conversation."
                        summary = model.generate(summary_prompt, conversation)
                        # Reset conversation with summary
                        conversation = [
                            {"role": "system", "content": "The following is a summary of the conversation so far: " + summary},
                            {"role": "system", "content": "Continue the conversation based on this summary."}
                        ]
                        token_count = count_tokens(str(conversation))
                        console.print(f"[green]Conversation compacted. New token count: {token_count}[/green]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted. Type '/exit' to quit or continue chatting.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

def show_help():
    """Show help information for interactive mode."""
    help_text = """
# Gemini Code Commands

## Built-in Commands
- `/exit` - Exit the chat session
- `/help` - Show this help message
- `/compact` - Summarize the conversation to reduce token usage

## CLI Commands (run outside the chat session)
- `gemini list-models` - List all available Gemini models
- `gemini setup YOUR_API_KEY` - Set up your Google API key
- `gemini set-default-model MODEL_NAME` - Set the default model
- `gemini --model MODEL_NAME` - Start chat with a specific model

## Available Tools
The assistant has access to various tools that it can use to help answer your questions:
- File operations (view, edit, ls, grep, glob)
- System commands (bash)
- Web content fetching (web)

Just ask questions normally, and the assistant will use these tools when needed.
    """
    console.print(Markdown(help_text))

if __name__ == "__main__":
    cli()