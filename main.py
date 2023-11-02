import os
import sys

import inquirer
from pystyle import *
from colorama import *
from downedit.site.douyin import __main__ as douyin
from downedit.site.kuaishou import __main__ as kuaishou
from downedit.site.tiktok import __main__ as tiktok
from downedit.video import __main__ as video_edit


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
                    Created by HengSok - v2.0
            """

    print(Center.XCenter(txt))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube("Use arrow key to select the options"))


def main():
    while True:
        try:
            display_banner()
            questions = [inquirer.List('list', message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=[
                ' Edit Video', ' Download Douyin Video', ' Download Tiktok Video', ' Download Kuaishou Video', ' Exit'])]
            answers = inquirer.prompt(questions)

            if answers['list'] == ' Edit Video':
                video_edit.main()
            elif answers['list'] == ' Download Douyin Video':
                douyin.main()
            elif answers['list'] == ' Download Tiktok Video':
                tiktok.main()
            elif answers['list'] == ' Download Kuaishou Video':
                kuaishou.main()
            elif answers['list'] == ' Exit':
                break
        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
            print(input(
                f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
