import os
import time

from pystyle import *
from colorama import *
from downedit.common import *


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
    banner_msg = "Type something you want to generate"
    return banner_display, banner_msg


def main():
    
    img_gen_prnt_path = Common.ensure_or_create_directory(IMG_GEN)
    banner_display, banner_msg = display_banner()
    print(Center.XCenter(banner_display))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube(banner_msg))
    user_input = input(f"{Fore.YELLOW}Enter Prompt:{Fore.WHITE} ")

if __name__ == "__main__":
    main()
