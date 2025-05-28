import logging
import aiohttp
import asyncio
from typing import Dict, Optional
from ratelimit import limits, sleep_and_retry
from rich.console import Console
import validators

logger = logging.getLogger(__name__)
console = Console()

class GraphQLTester:
    """Tests GraphQL endpoints for vulnerabilities."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.introspection_query = '''
        {
          __schema {
            types {
              name
            }
          }
        }
        '''
    
    @sleep_and_retry
    @limits(calls=5, period=1)
    async def test_endpoint(self, url: str) -> Dict:
        """Test a GraphQL endpoint for introspection."""
        try:
            if not validators.url(url):
                raise ValueError("Invalid URL")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={"query": self.introspection_query}) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "__schema" in data.get("data", {}):
                            console.print("[red][!] Introspection enabled[/red]")
                            return {"url": url, "introspection_enabled": True}
                        else:
                            console.print("[green][+] Introspection disabled[/green]")
                            return {"url": url, "introspection_enabled": False}
                    else:
                        logger.warning(f"GraphQL test failed: {response.status}")
                        return {"url": url, "error": "Failed to connect"}
        except Exception as e:
            logger.error(f"GraphQL test failed: {e}")
            return {"url": url, "error": str(e)}