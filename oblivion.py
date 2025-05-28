import logging
import sys
from pathlib import Path
import yaml
import click
from rich.console import Console
from injector import Injector
from core.di import configure_di
from core.banner import display_banner
from core.menu import main_menu
from core.runner import Runner
from core.plugin_loader import PluginLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('reports/oblivion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
console = Console()

# Configuration file
CONFIG_FILE = Path('config/settings.yaml')
DEFAULT_CONFIG = {
    'output_dir': 'reports',
    'shodan_api_key': '',
    'default_timeout': 10,
    'rate_limit': 5,
    'ethical_use_agreed': False,
}

def load_config() -> dict:
    """Load configuration from YAML file or create default if not exists."""
    try:
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open('r') as f:
                return yaml.safe_load(f)
        else:
            CONFIG_FILE.parent.mkdir(exist_ok=True)
            with CONFIG_FILE.open('w') as f:
                yaml.safe_dump(DEFAULT_CONFIG, f)
            return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return DEFAULT_CONFIG

def create_directories(config: dict) -> None:
    """Create necessary directories."""
    try:
        Path(config['output_dir']).mkdir(exist_ok=True)
        Path(config['output_dir']).joinpath('web').mkdir(exist_ok=True)
        Path(config['output_dir']).joinpath('shodan').mkdir(exist_ok=True)
        Path('plugins').mkdir(exist_ok=True)
        Path('tests').mkdir(exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directories: {e}")

def ensure_ethical_use(config: dict) -> None:
    """Prompt user to agree to ethical use guidelines."""
    if not config.get('ethical_use_agreed', False):
        console.print("[bold red]WARNING: Oblivion is for authorized testing only.[/bold red]")
        if click.confirm("Do you agree to use Oblivion ethically and only on systems you have permission to test?"):
            config['ethical_use_agreed'] = True
            with CONFIG_FILE.open('w') as f:
                yaml.safe_dump(config, f)
        else:
            console.print("[bold red]You must agree to ethical use to proceed.[/bold red]")
            sys.exit(1)

@click.group()
def cli():
    """Oblivion v3.0: A modern web penetration testing tool."""
    pass

@cli.command()
def start():
    """Start the Oblivion tool."""
    try:
        config = load_config()
        ensure_ethical_use(config)
        create_directories(config)
        injector = Injector(configure_di(config))
        runner = injector.get(Runner)
        plugin_loader = injector.get(PluginLoader)
        plugin_loader.load_plugins(cli)
        display_banner()
        main_menu(runner)
    except KeyboardInterrupt:
        console.print("[yellow]Exiting Oblivion[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    cli()