import os
import sys

import inquirer
from pystyle import *
from colorama import *
from downedit.site.douyin import __main__ as douyin
from downedit.site.kuaishou import __main__ as kuaishou
from downedit.site.tiktok import __main__ as tiktok
from downedit.common import DE_VERSION

def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    os.system("title DownEdit" if os.name == "nt" else "")
    txt = f"""{Fore.MAGENTA}
██╗░░░██╗██╗██████╗░░░░░░░██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗
██║░░░██║██║██╔══██╗░░░░░░██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║
╚██╗░██╔╝██║██║░░██║█████╗██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║
░╚████╔╝░██║██║░░██║╚════╝██║░░██║██║░░██║░░████╔═████║░██║╚████║
░░╚██╔╝░░██║██████╔╝░░░░░░██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║
░░░╚═╝░░░╚═╝╚═════╝░░░░░░░╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝
                    Created by HengSok - v{DE_VERSION}
            """

    print(Center.XCenter(txt))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube("Use arrow key to select the options"))


def main():
    try:
        display_banner()
        questions = [inquirer.List('list', message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=[
            ' Douyin', ' Tiktok', ' Kuaishou', ' Back'])]
        answers = inquirer.prompt(questions)

        if answers['list'] == ' Douyin':
            douyin.main()
        elif answers['list'] == ' Tiktok':
            tiktok.main()
        elif answers['list'] == ' Kuaishou':
            kuaishou.main()
        elif answers['list'] == ' Back':
            return
    except Exception as e:
        print(
            f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
        print(input(
            f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()