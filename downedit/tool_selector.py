import os
from colorama import Fore
import inquirer
from pystyle import *
from colorama import *


class ToolSelector:
    def __init__(self) -> None:
        pass

    def display_banner(self, banner, message):
        os.system('cls')
        print(Center.XCenter(banner))
        print(f'{Fore.GREEN}')
        print(Box.DoubleCube(message))

    def site_manual_select(self, banner, message):
        self.display_banner(banner=banner, message=message)
        questions = [
            inquirer.List(
                'list',
                message=f"{Fore.YELLOW}Select Option{Fore.WHITE}",
                choices=[
                    ' Single User',
                    ' Batch Users',
                    ' Exit'
                ]
            )
        ]

        answers = inquirer.prompt(questions)
        return answers['list']

    def single_user_select(self, banner, message):

        self.display_banner(banner=banner, message=message)
        user_input = input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")
        if user_input is None:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Please Enter User Name!")
        return user_input

    def batch_user_select(self, banner, message):
        
        self.display_banner(banner=banner, message=message)
        file_path = input(f"{Fore.YELLOW}Enter File Path:{Fore.WHITE} ")
        if file_path is None:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Please Enter File Path!")
        try:
            with open(file_path, 'r') as file:
                users = file.readlines()
                users = [user.strip() for user in users]
                return users
        except FileNotFoundError:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}File not found or could not be opened.")
            return []


if __name__ == "__main__":
    tool_selector = ToolSelector()
