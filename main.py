import os
import sys

import inquirer
from pystyle import *
from colorama import *
from downedit.site import __main__ as vid_dl
from downedit.image import __main__ as gen_img_ai
from downedit.video import __main__ as video_edit
from downedit.common import DE_VERSION

def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    os.system("title DownEdit" if os.name == "nt" else "")
    txt = f"""{Fore.MAGENTA}
██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗░░░░░░███████╗██████╗░██╗████████╗
██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║░░░░░░██╔════╝██╔══██╗██║╚══██╔══╝
██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║█████╗█████╗░░██║░░██║██║░░░██║░░░
██║░░██║██║░░██║░░████╔═████║░██║╚████║╚════╝██╔══╝░░██║░░██║██║░░░██║░░░
██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║░░░░░░███████╗██████╔╝██║░░░██║░░░
╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝░░░░░░╚══════╝╚═════╝░╚═╝░░░╚═╝░░░
                      Created by HengSok - v{DE_VERSION}
            """

    print(Center.XCenter(txt))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube("Use arrow key to select the options"))


def main():
    while True:
        try:
            display_banner()
            questions = [inquirer.List('list', message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=[
                ' Edit Video', ' Download Video', ' AI-Generative Image', ' Exit'])]
            answers = inquirer.prompt(questions)

            if answers['list'] == ' Edit Video':
                video_edit.main()
            elif answers['list'] == ' Download Video':
                vid_dl.main()
            elif answers['list'] == ' AI-Generative Image':
                gen_img_ai.main()
            elif answers['list'] == ' Exit':
                break
        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
            print(input(
                f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
