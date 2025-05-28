from injector import Binder, Injector, singleton
import logging
from typing import Dict
from modules.recon.subdomain import SubdomainScanner
from modules.web.graphql import GraphQLTester
from modules.brute.login import LoginBruteforcer
from modules.osint.social import SocialProfiler
from modules.utils.generator import Generator
from modules.reports.report import ReportGenerator
from core.plugin_loader import PluginLoader

def configure_di(config: Dict):
    def configure(binder: Binder) -> None:
        binder.bind(logging.Logger, to=logging.getLogger(__name__), scope=singleton)
        binder.bind(Dict, to=config, scope=singleton)
        binder.bind(SubdomainScanner, to=SubdomainScanner(config), scope=singleton)
        binder.bind(GraphQLTester, to=GraphQLTester(config), scope=singleton)
        binder.bind(LoginBruteforcer, to=LoginBruteforcer(config), scope=singleton)
        binder.bind(SocialProfiler, to=SocialProfiler(config), scope=singleton)
        binder.bind(Generator, to=Generator(config), scope=singleton)
        binder.bind(ReportGenerator, to=ReportGenerator(config), scope=singleton)
        binder.bind(PluginLoader, to=PluginLoader(config), scope=singleton)
    return configure