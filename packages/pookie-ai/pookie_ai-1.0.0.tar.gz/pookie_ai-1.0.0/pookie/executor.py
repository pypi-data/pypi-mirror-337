import subprocess
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def execute_command(command):
    """
    Execute a shell command with confirmation options:
    - [y] to execute
    - [n] to abort
    - [q] to edit before executing
    """
    while True:
        console.print("[bold green]To execute, press y [/bold green]")
        console.print("[bold red]To abort, press n [/bold red]")
        console.print("[bold yellow]To edit, press q [/bold yellow]")

        choice = Prompt.ask("[bold cyan]Your choice (y/n/q)[/bold cyan]").strip().lower()

        if choice == "y":
            # Execute the command
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.stdout.strip():
                    console.print("\n[bold green]✅ Output:[/bold green]")
                    console.print(result.stdout)
                elif result.stderr:
                    console.print(f"[bold red]❌ Error:[/bold red] {result.stderr}")
                else:
                    console.print("\n[bold green]✅ Command executed successfully![/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Failed to execute command:[/bold red] {e}")
            break

        elif choice == "n":
            console.print("[bold yellow]🚫 Aborted command execution.[/bold yellow]")
            break

        elif choice == "q":
            # Edit the command before executing
            new_command = Prompt.ask("[bold cyan]Edit the command[/bold cyan]", default=command)
            command = new_command.strip()

        else:
            console.print("[bold red]❌ Invalid option. Please select [y], [n], or [q].[/bold red]")
