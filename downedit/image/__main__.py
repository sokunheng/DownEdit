import os
import time

from pystyle import *
from colorama import *
from downedit.common import *
from downedit.site.enterpix import __main__ as enterpix

def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    os.system("title DownEdit" if os.name == "nt" else "")
    banner_display = f"""{Fore.MAGENTA} 
░█████╗░██╗  ██╗███╗░░░███╗░█████╗░░██████╗░███████╗░░░░░░░██████╗░███████╗███╗░░██╗
██╔══██╗██║  ██║████╗░████║██╔══██╗██╔════╝░██╔════╝░░░░░░██╔════╝░██╔════╝████╗░██║
███████║██║  ██║██╔████╔██║███████║██║░░██╗░█████╗░░█████╗██║░░██╗░█████╗░░██╔██╗██║
██╔══██║██║  ██║██║╚██╔╝██║██╔══██║██║░░╚██╗██╔══╝░░╚════╝██║░░╚██╗██╔══╝░░██║╚████║
██║░░██║██║  ██║██║░╚═╝░██║██║░░██║╚██████╔╝███████╗░░░░░░╚██████╔╝███████╗██║░╚███║
╚═╝░░╚═╝╚═╝  ╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚═════╝░╚══════╝░░░░░░░╚═════╝░╚══════╝╚═╝░░╚══╝
                            Created by HengSok - v{DE_VERSION}
    """
    banner_msg = "Select Models to generate images"
    return banner_display, banner_msg


def main():
    while True:
        banner_display, banner_msg = display_banner()
        print(Center.XCenter(banner_display))
        print(f'{Fore.GREEN}')
        print(Box.DoubleCube(banner_msg))
        questions = [inquirer.List('list', message=f"{Fore.YELLOW}Select Models{Fore.WHITE}", choices=[
                        ' Enterpix', ' Back'])]
        answers = inquirer.prompt(questions)
        selected_tool = answers['list']
        
        if selected_tool == ' Enterpix':
            enterpix.main()
        elif selected_tool == ' Back':
            break

if __name__ == "__main__":
    main()
