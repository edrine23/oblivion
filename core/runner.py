import logging
import click
from typing import Dict
from injector import inject
from rich.console import Console
from modules.recon.subdomain import SubdomainScanner
from modules.web.graphql import GraphQLTester
from modules.brute.login import LoginBruteforcer
from modules.osint.social import SocialProfiler
from modules.utils.generator import Generator
from modules.reports.report import ReportGenerator

logger = logging.getLogger(__name__)
console = Console()

class Runner:
    """Manages execution of Oblivion modules."""
    
    @inject
    def __init__(self, config: Dict, subdomain_scanner: SubdomainScanner,
                 graphql_tester: GraphQLTester, login_bruteforcer: LoginBruteforcer,
                 social_profiler: SocialProfiler, generator: Generator,
                 report_generator: ReportGenerator):
        self.config = config
        self.subdomain_scanner = subdomain_scanner
        self.graphql_tester = graphql_tester
        self.login_bruteforcer = login_bruteforcer
        self.social_profiler = social_profiler
        self.generator = generator
        self.report_generator = report_generator
    
    def web_pentest_menu(self) -> None:
        """Web pentest menu."""
        @click.command()
        @click.option('--domain', type=str, required=True, help='Target domain')
        def subdomain_scan(domain: str) -> None:
            try:
                console.print(f"[cyan]Scanning subdomains for {domain}[/cyan]")
                results = self.subdomain_scanner.scan(domain)
                self.report_generator.add_results("subdomain_scan", results)
                console.print("[green]Scan complete. Results saved.[/green]")
            except Exception as e:
                logger.error(f"Subdomain scan failed: {e}")
                console.print(f"[red]Error: {e}[/red]")
        
        ctx = click.get_current_context()
        ctx.invoke(subdomain_scan)
    
    def web_attack_menu(self) -> None:
        """Web attack menu."""
        @click.command()
        @click.option('--url', type=str, required=True, help='Target URL')
        def graphql_test(url: str) -> None:
            try:
                console.print(f"[cyan]Testing GraphQL at {url}[/cyan]")
                results = self.graphql_tester.test_endpoint(url)
                self.report_generator.add_results("graphql_test", results)
                console.print("[green]Test complete. Results saved.[/green]")
            except Exception as e:
                logger.error(f"GraphQL test failed: {e}")
                console.print(f"[red]Error: {e}[/red]")
        
        ctx = click.get_current_context()
        ctx.invoke(graphql_test)
    
    def brute_menu(self) -> None:
        """Brute force menu."""
        @click.command()
        @click.option('--url', type=str, required=True, help='Login form URL')
        @click.option('--wordlist', type=str, required=True, help='Path to wordlist')
        def brute_login(url: str, wordlist: str) -> None:
            try:
                console.print(f"[cyan]Brute-forcing login at {url}[/cyan]")
                results = self.login_bruteforcer.brute_force(url, wordlist)
                self.report_generator.add_results("brute_login", results)
                console.print("[green]Brute force complete. Results saved.[/green]")
            except Exception as e:
                logger.error(f"Brute force failed: {e}")
                console.print(f"[red]Error: {e}[/red]")
        
        ctx = click.get_current_context()
        ctx.invoke(brute_login)
    
    def osint_menu(self) -> None:
        """OSINT menu."""
        @click.command()
        @click.option('--username', type=str, required=True, help='Target username')
        def social_profile(username: str) -> None:
            try:
                console.print(f"[cyan]Profiling {username}[/cyan]")
                results = self.social_profiler.profile(username)
                self.report_generator.add_results("social_profile", results)
                console.print("[green]Profiling complete. Results saved.[/green]")
            except Exception as e:
                logger.error(f"Social profiling failed: {e}")
                console.print(f"[red]Error: {e}[/red]")
        
        ctx = click.get_current_context()
        ctx.invoke(social_profile)
    
    def utils_menu(self) -> None:
        """Utilities menu."""
        @click.command()
        @click.option('--length', type=int, default=12, help='Length of random password')
        @click.option('--text', type=str, default='password', help='Text to hash and convert')
        def generate_password(length: int, text: str) -> None:
            try:
                random_pass, md5_hash, leet_text = self.generator.password_generator(length, text)
                console.print(f"[green][+] Random Password: {random_pass}[/green]")
                console.print(f"[green][+] MD5 Hash: {md5_hash}[/green]")
                console.print(f"[green][+] Leet Speak: {leet_text}[/green]")
                self.report_generator.add_results("generator", {
                    "password": random_pass, "md5_hash": md5_hash, "leet_text": leet_text
                })
            except Exception as e:
                logger.error(f"Password generation failed: {e}")
                console.print(f"[red]Error: {e}[/red]")
        
        ctx = click.get_current_context()
        ctx.invoke(generate_password)