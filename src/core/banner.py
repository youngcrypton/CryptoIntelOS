from rich.console import Console

console = Console()


def show_banner():

    console.print("=" * 50, style="cyan")

    console.print(
        "CryptoIntel OS",
        style="bold green",
    )

    console.print(
        "Your Personal Crypto Intelligence Platform",
        style="yellow",
    )

    console.print("=" * 50, style="cyan")