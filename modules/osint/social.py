import logging
import aiohttp
import asyncio
from typing import Dict, List
from ratelimit import limits, sleep_and_retry
from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()

class SocialProfiler:
    """Profiles usernames across social platforms."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.platforms = {
            "twitter": "https://api.twitter.com/2/users/by/username/{}",
            # Add more platforms
        }
    
    @sleep_and_retry
    @limits(calls=5, period=1)
    async def check_platform(self, session: aiohttp.ClientSession, platform: str, username: str) -> Dict:
        """Check if username exists on a platform."""
        try:
            url = self.platforms[platform].format(username)
            async with session.get(url, headers={"Authorization": f"Bearer {self.config.get('twitter_api_key', '')}"}) as response:
                if response.status == 200:
                    console.print(f"[green][+] Found {username} on {platform}[/green]")
                    return {"platform": platform, "username": username, "exists": True}
                return {"platform": platform, "username": username, "exists": False}
        except Exception as e:
            logger.error(f"Platform check failed: {e}")
            return {"platform": platform, "username": username, "exists": False}
    
    async def profile(self, username: str) -> List[Dict]:
        """Profile a username across platforms."""
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.check_platform(session, platform, username) for platform in self.platforms]
            results = await asyncio.gather(*tasks)
        return results