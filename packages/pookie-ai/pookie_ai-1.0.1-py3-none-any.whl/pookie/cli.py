import argparse
from rich.console import Console
from rich.prompt import Prompt
from pookie.config import save_api_key, load_api_key, check_first_time_setup
from pookie.gemini_api import init_gemini,get_command
from . import initialize_gemini
from pookie.executor import execute_command
console = Console()

def setup():
    """Initial setup to store Gemini API key."""
    api_key = Prompt.ask("[bold cyan]Enter your Gemini API key[/bold cyan]")
    
    if api_key:
        save_api_key(api_key)
        console.print("[bold green]✅ API key saved successfully![/bold green]")
    else:
        console.print("[bold red]❌ No API key provided. Exiting...[/bold red]")

def run_pookie():
    """Main CLI entry point."""
    # Check for first-time setup
    if not check_first_time_setup():
        console.print("[bold yellow]⚠️ No API key found. Please run `pookie setup`.[/bold yellow]")
        return
    # Display welcome message
    console.print("[bold magenta]🐾 Welcome to Pookie! 🐾[/bold magenta]")
    console.print("[bold cyan]Use `pookie setup` to reconfigure the API key.[/bold cyan]")

    while True:
        prompt = Prompt.ask("[bold cyan]Pookie >[/bold cyan]")

        if prompt.lower() in ["exit", "quit"]:
            console.print("[bold yellow]👋 Goodbye![/bold yellow]")
            break

        command = get_command(prompt)

        console.print(f"[bold green]🤖 Received command:[/bold green] {command}")
        #Ask for confirmation and execute command.
        execute_command(command)



def main():
    parser = argparse.ArgumentParser(description="Pookie: Your terminal AI assistant")
    parser.add_argument("command",nargs="*" , help="Command to run (e.g., setup)")
    
    args = parser.parse_args()

    api_key = initialize_gemini()
    
    if args.command:
        if args.command[0] == "setup":
            setup()
            return
        if not check_first_time_setup():
            console.print("[bold yellow]⚠️ No API key found. Please run `pookie setup`.[/bold yellow]")
            return 
        prompt = ' '.join(args.command)
        command = get_command(prompt)
        console.print(f"\n🤖 [bold cyan]Generated Command:[/bold cyan] {command}")  
        execute_command(command) #ask for confirmation and execute
    else:
        run_pookie()

if __name__ == "__main__":
    main()

