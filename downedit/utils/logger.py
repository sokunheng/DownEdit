import colorama

from colorama import Fore
from rich.traceback import install
from rich.console import Console

install()
console = Console()

class Logger:
    def __init__(self, name=None):
        self.name = name
    
    def time(self, time, info, message):
        print(
            f"\n{Fore.CYAN}[{time}] {Fore.YELLOW}[{info}] {Fore.WHITE}",
            message
        )
        
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
    
    def keybind(self, message):
        print(
            input(
                f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}{message}"
        ))
    
    def folder_info(self, message):
        console.log(
            "[red][FOLDER][/red]",
            message
        ) 
        
    def folder_error(self, message):
        console.log(
            "[red][FOLDER][/red]",
            message
        ) 
        
    def file_info(self, message):
        console.log(
            "[cyan][FILE][/cyan]",
            message
        )
        
    def file_error(self, message):
        console.log(
            "[red][FILE][/red]",
            message
        )