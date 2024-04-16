import colorama

from colorama import Fore
from rich.traceback import install
from rich.console import Console

install()
console = Console()

class Logger:
    def __init__(self, name=None):
        self.name = name

    def info(self, message):
        print(
            f"\n{Fore.CYAN}[{self.name}] {Fore.YELLOW}[Status]{Fore.WHITE}",
            message
        )

    def error(self, message):
        print(
            f"\n{Fore.CYAN}[{self.name}] {Fore.YELLOW}[Error]{Fore.RED}",
            message
        )
    
    def folder_info(self, message):
        console.log(
            "[red][Folder][/red]",
            message
        ) 
        
    def folder_error(self, message):
        console.log(
            "[red][Folder][/red]",
            message
        ) 
        
    def file_info(self, message):
        console.log(
            "[red][Folder][/red]",
            message
        )
        
    def file_error(self, message):
        console.log(
            "[red][Folder][/red]",
            message
        )