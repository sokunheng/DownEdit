import os
from colorama import Fore
import inquirer
from pystyle import *
from colorama import *


class ToolSelector:
    def __init__(self) -> None:
        self.running = True
    
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
            
            functions[selected]()

    def site_manual_select(self, banner, message):
        self.display_banner(banner=banner, message=message)
        choices = [ ' Single User', ' Batch Users', ' Exit' ]
        question = self.select_menu(
            message=f"{Fore.YELLOW}Select Option{Fore.WHITE}",
            choices=choices
        )
        return question

    def single_user_select(self, banner, message):

        self.display_banner(banner=banner, message=message)
        user_input = input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")
        if user_input is None:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Please Enter User Name!"
            )
        return user_input

    def batch_user_select(self, banner, message):

        self.display_banner(banner=banner, message=message)
        file_path = input(f"{Fore.YELLOW}Enter File Path:{Fore.WHITE} ")
        if file_path is None:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Please Enter File Path!"
            )
        try:
            with open(file_path, 'r') as file:
                users = file.readlines()
                users = [user.strip() for user in users]
                return users
        except FileNotFoundError:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}File not found or could not be opened."
            )
            return []