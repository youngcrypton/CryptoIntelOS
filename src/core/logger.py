from rich.console import Console

console = Console()


def initialize_logger():
    """Initialize the application logger."""
    console.print("[green]✓ Logger initialized[/green]")