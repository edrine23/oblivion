import logging
import random
from typing import Tuple, Dict, List
import hashlib
import jwt
from rich.console import Console
import jinja2

logger = logging.getLogger(__name__)
console = Console()

class Generator:
    """Handles password, hash, payload, and JWT functionalities."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.chars = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[{}];:"\|,<.>/?`~'
        self.env = jinja2.Environment(loader=jinja2.DictLoader({
            "xss_payload": "<script>{{ payload }}</script>"
        }))
    
    def password_generator(self, length: int, text: str) -> Tuple[str, str, str]:
        """Generate random password, MD5 hash, and leet-speak version of text."""
        try:
            if length < 1:
                raise ValueError("Password length must be positive")
            if not text:
                raise ValueError("Input text cannot be empty")
            
            random_password = ''.join(random.choice(self.chars) for _ in range(length))
            md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            leet_alphabet = {
                'a': '4', 'b': '8', 'c': '(', 'd': '|)', 'e': '3', 'f': '|=',
                'g': '9', 'h': '#', 'i': '1', 'j': '_|', 'k': '|<', 'l': '|_',
                'm': r'|\/|', 'n': r'|\|', 'o': '0', 'p': '|D', 'q': '(,)', 'r': '|2',
                's': '$', 't': '7', 'u': '|_|', 'v': r'\/', 'w': r'\/\/', 'x': '><',
                'y': r'\'/', 'z': '(/)'
            }
            leet_text = text.lower()
            for char, leet in leet_alphabet.items():
                leet_text = leet_text.replace(char, leet)
            
            return random_password, md5_hash, leet_text
        except Exception as e:
            logger.error(f"Password generation failed: {e}")
            raise
    
    def generate_payload(self, payload_type: str, value: str) -> str:
        """Generate attack payloads using templates."""
        try:
            if payload_type == "xss":
                template = self.env.get_template("xss_payload")
                return template.render(payload=value)
            raise ValueError("Unsupported payload type")
        except Exception as e:
            logger.error(f"Payload generation failed: {e}")
            raise
    
    def test_jwt(self, token: str) -> Dict:
        """Decode and test JWT for vulnerabilities."""
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            if decoded.get("alg") == "none":
                console.print("[red][!] Vulnerable: alg=none detected[/red]")
            return {"decoded": decoded, "vulnerable": decoded.get("alg") == "none"}
        except Exception as e:
            logger.error(f"JWT test failed: {e}")
            return {"error": str(e)}