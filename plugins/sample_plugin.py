from core.plugin_loader import Plugin
import click
from rich.console import Console

console = Console()

class SamplePlugin(Plugin):
    """Sample plugin for Oblivion v3.0."""
    
    def __init__(self, config: dict):
        self.config = config
    
    def execute(self, args: dict) -> None:
        console.print(f"[cyan]Executing sample plugin with args: {args}[/cyan]")
    
    def register_commands(self, cli_group: click.Group) -> None:
        @cli_group.command(name="sample")
        @click.option('--target', type=str, help='Target to process')
        def sample_command(target: str) -> None:
            self.execute({"target": target})