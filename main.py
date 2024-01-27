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
            choices = [ ' Edit Video',
                       f' AI Edit Video {Fore.RED}(Soon)',
                       f' Edit Photo {Fore.RED}(Soon)',
                       f' AI Edit Photo {Fore.RED}(Soon)',
                        ' Download Video',
                        ' AI-Generative Image',
                       f' AI-Generative Video {Fore.RED}(Soon)',
                        ' Exit']

            questions = [inquirer.List(
                'list', message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=choices)]
            answers = inquirer.prompt(questions)
            selected_tool = answers['list']

            if selected_tool == ' Edit Video':
                video_edit.main()
            elif selected_tool == ' AI Edit Video (Soon)':
                pass
            elif selected_tool == ' Edit Photo (Soon)':
                pass
            elif selected_tool == ' AI Edit Photo (Soon)':
                pass
            elif selected_tool == ' Download Video':
                vid_dl.main()
            elif selected_tool == ' AI-Generative Image':
                gen_img_ai.main()
            elif selected_tool == ' AI-Generative Video (Soon)':
                pass
            elif selected_tool == ' Exit':
                break
        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
            print(input(
                f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
