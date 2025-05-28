from rich.console import Console

console = Console()

def display_banner() -> None:
    """Display the Oblivion banner."""
    console.print("""
[bold cyan]
╔════════════════════════════════════╗
║         Oblivion v3.0              ║
║   Web Penetration Testing Tool     ║
║   Author: Cr4sHCoD3                ║
║   Ethical Use Only: Test with      ║
║   explicit permission only!        ║
╚════════════════════════════════════╝
[/bold cyan]
    """)