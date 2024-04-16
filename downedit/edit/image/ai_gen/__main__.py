import os
import time

from pystyle import *
from colorama import *
from downedit.utils.common import *
from downedit.site.enterpix import __main__ as enterpix
from downedit.site.lexica import __main__ as lexica

def display_banner():
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
    while tool_selector.running:
        banner_display, banner_msg = display_banner()
        tool_selector.display_banner(banner_display, banner_msg, "- generative ai")
        
        choices = [" Stable Diffusion", " Lexica Aperture", " Back"]
        selected_tool = tool_selector.select_menu(message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=choices)
        menu_list = {
            " Stable Diffusion": enterpix.main,
            " Lexica Aperture": lexica.main,
            " Back": lambda: None
        }
        
        tool_selector.execute_menu(selected_tool, menu_list)

if __name__ == "__main__":
    main()
