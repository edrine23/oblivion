import logging
import aiohttp
import asyncio
from typing import Dict, List
from ratelimit import limits, sleep_and_retry
from rich.console import Console
import validators

logger = logging.getLogger(__name__)
console = Console()

class SubdomainScanner:
    """Scans for subdomains using passive sources."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_endpoints = {
            "virustotal": "https://www.virustotal.com/vtapi/v2/domain/report"
        }
    
    @sleep_and_retry
    @limits(calls=5, period=1)
    async def fetch_subdomains(self, session: aiohttp.ClientSession, domain: str) -> List[str]:
        """Fetch subdomains from VirusTotal API."""
        try:
            if not validators.domain(domain):
                raise ValueError("Invalid domain")
            params = {"domain": domain, "apikey": self.config.get("virustotal_api_key", "")}
            async with session.get(self.api_endpoints["virustotal"], params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("subdomains", [])
                else:
                    logger.warning(f"Failed to fetch subdomains: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Subdomain fetch failed: {e}")
            return []
    
    async def scan(self, domain: str) -> List[Dict]:
        """Scan for subdomains."""
        results = []
        async with aiohttp.ClientSession() as session:
            subdomains = await self.fetch_subdomains(session, domain)
            for subdomain in subdomains:
                results.append({"subdomain": subdomain, "domain": domain})
                console.print(f"[green][+] Found: {subdomain}[/green]")
        return results