import os
import inquirer

from colorama import Fore
from pystyle import *
from colorama import *
from abc import ABC, abstractmethod

from .logger import Logger 

logger = Logger("Programs")

class UserInput(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def get_user_input(self, message):
        pass

    @abstractmethod
    def select_input(self, tool_selector, banner, message):
        pass  

class SingleInput(UserInput):
    def get_user_input(self, message):
        return input(message)
    
    def select_input(self, tool_selector, banner, message):
        tool_selector.display_banner(banner, message)
        user_input = self.get_user_input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")
        if not user_input:
            logger.error("Please Enter Username!")
            return
        return user_input

class BatchInput(UserInput):
    def get_user_input(self, message):
        return input(message)

    def select_input(self, tool_selector, banner, message):
        tool_selector.display_banner(banner, message)
        file_path = self.get_user_input(f"{Fore.YELLOW}Enter File Path:{Fore.WHITE} ")
        if not file_path:
            logger.error("Please Enter File Path!")
            return
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                return lines
        except FileNotFoundError:
            logger.error("File not found or could not be opened.")
            return []

class ToolSelector:
    def __init__(self) -> None:
        self.running = True
        self._user_input = None
    
    def set_user_input(self, selection: UserInput):
        self._user_input = selection
    
    def get_user_input(self, message):
        if self._user_input is None:
            raise ValueError("User input strategy not set")
        return self._user_input.get_user_input(message)
    
    def show_box(self, message):
        print(f'{Fore.GREEN}')
        print(Box.DoubleCube(message))

    def display_banner(self, banner, message, title=None):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title DownEdit {title}" if os.name == "nt" else "")
        print(Center.XCenter(banner))
        self.show_box(message)

    def select_menu(self, message, choices):
        questions = [
            inquirer.List(
                'list',
                message=message,
                choices=choices
            )
        ]
        answers = inquirer.prompt(questions)
        return answers['list']

    def execute_menu(self, selected, functions):
        if selected in functions:
            if selected == " Back":
                self.running = False
                return
            functions[selected].execute()

    def manual_select(
        self,
        menu_options: dict,
        banner,
        message,
    ):
        self.display_banner(banner=banner, message=message)
        question = self.select_menu(
            message=f"{Fore.YELLOW}Select Option{Fore.WHITE}",
            choices=menu_options
        )
        return question
    
    def selection_input(
        self,
        strategy: UserInput,
        banner,
        message
    ):
        return strategy.select_input(self, banner, message)
        
    def start(
        self,
        menu_options: dict,
        input_message: str,
    ) -> None:
        """
        Starts the tool selection process.
        """
        chosen_tool = self.select_menu(
            message=input_message,
            choices=list(menu_options.keys())
        )
        self.execute_menu(
            chosen_tool,
            menu_options
        )

