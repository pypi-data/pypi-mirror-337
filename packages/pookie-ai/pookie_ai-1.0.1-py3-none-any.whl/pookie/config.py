import os
from pathlib import Path
from rich.console import Console

CONFIG_FILE = Path.home() / ".pookie_config"
console = Console()

def save_api_key(api_key):
    """Save Gemini API key to a config file."""
    try:
        with open(CONFIG_FILE, "w") as file:
            file.write(api_key)
        console.print("[bold green]✅ API key saved successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to save API key: {str(e)}[/bold red]")

def load_api_key():
    """Load the saved Gemini API key from the config file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as file:
            return file.read().strip()
    return None

def check_first_time_setup():
    """Check if the API key is already configured."""
    if not CONFIG_FILE.exists():
        return False
    return True
