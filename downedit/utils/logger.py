import time
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
        """
        Print a message with a timestamp.
        
        Args:
            time (str): The timestamp.
            info (str): The type of message.
            message (str): The message to print.
        
        Returns:
            None
        """
        print(
            f"\n{Fore.CYAN}[{time}] {Fore.YELLOW}[{info}] {Fore.WHITE}",
            message
        )
        
    def info(self, message):
        """
        Print an information message.
        
        Args:
            message (str): The message to print.
        
        Returns:
            None
        """
        print(
            f"\n{Fore.CYAN}[{self.name}] {Fore.YELLOW}[Status]{Fore.WHITE}",
            message
        )

    def error(self, message):
        """
        Print an error message.
        
        Args:
            message (str): The message to print.
            
        Returns:
            None
        """
        print(
            f"\n{Fore.CYAN}[{self.name}] {Fore.YELLOW}[Error]{Fore.RED}",
            message
        )
    
    def keybind(self, message):
        """
        Print a keybinding message.
        
        Args:
            message (str): The message to print.
            
        Returns:
            None
        """
        print(
            input(
                f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}{message}"
        ))
    
    def folder_info(self, message):
        """
        Print a folder information message.
        
        Args:
            message (str): The message to print.
            
        Returns:
            None
        """
        time.sleep(0.5)
        console.log(
            "[red][FOLDER][/red]",
            message
        ) 
        
    def folder_error(self, message):
        """
        Print a folder error message.
        
        Args:
            message (str): The message to print.
        
        Returns:
            None
        """
        time.sleep(0.5)
        console.log(
            "[red][FOLDER][/red]",
            message
        ) 
        
    def file_info(self, message):
        """
        Print a file information message.
        
        Args:
            message (str): The message to print.
        
        Returns:
            None
        """
        time.sleep(1.0)
        console.log(
            "[cyan][FILE][/cyan]",
            message
        )
        
    def file_error(self, message):
        """
        Print a file error message.
        
        Args:
            message (str): The message to print.
        
        Returns:
            None
        """
        time.sleep(0.5)
        console.log(
            "[red][FILE][/red]",
            message
        )