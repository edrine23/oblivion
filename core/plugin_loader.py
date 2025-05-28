import logging
import importlib
from pathlib import Path
from typing import Dict, List
from abc import ABC, abstractmethod
import click
from RestrictedPython import compile_restricted, safe_globals

logger = logging.getLogger(__name__)

class Plugin(ABC):
    """Base class for Oblivion plugins."""
    @abstractmethod
    def execute(self, args: dict) -> None:
        pass

    @abstractmethod
    def register_commands(self, cli_group: click.Group) -> None:
        pass

class PluginLoader:
    """Loads and manages plugins from the plugins/ directory."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.plugins: List[Plugin] = []
    
    def load_plugins(self, cli_group: click.Group) -> None:
        """Load all plugins from the plugins/ directory."""
        plugins_dir = Path("plugins")
        plugins_dir.mkdir(exist_ok=True)
        for plugin_file in plugins_dir.glob("*.py"):
            try:
                module_name = plugin_file.stem
                if module_name == "__init__":
                    continue
                with open(plugin_file, 'r') as f:
                    code = f.read()
                compiled_code = compile_restricted(code, str(plugin_file), 'exec')
                safe_locals = {}
                exec(compiled_code, safe_globals, safe_locals)
                for attr in safe_locals.values():
                    if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                        plugin = attr(self.config)
                        self.plugins.append(plugin)
                        plugin.register_commands(cli_group)
                        logger.info(f"Loaded plugin: {module_name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file}: {e}")