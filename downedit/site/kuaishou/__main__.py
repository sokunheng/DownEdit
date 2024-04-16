
import os
import time

from pystyle import *
from colorama import *

from downedit.utils.common import *


def display_banner():
    banner_display = f"""{Fore.MAGENTA} 
██╗░░██╗██╗░░░██╗░█████╗░██╗░██████╗██╗░░██╗░█████╗░██╗░░░██╗░░░░░░██████╗░██╗░░░░░
██║░██╔╝██║░░░██║██╔══██╗██║██╔════╝██║░░██║██╔══██╗██║░░░██║░░░░░░██╔══██╗██║░░░░░
█████═╝░██║░░░██║███████║██║╚█████╗░███████║██║░░██║██║░░░██║█████╗██║░░██║██║░░░░░
██╔═██╗░██║░░░██║██╔══██║██║░╚═══██╗██╔══██║██║░░██║██║░░░██║╚════╝██║░░██║██║░░░░░
██║░╚██╗╚██████╔╝██║░░██║██║██████╔╝██║░░██║╚█████╔╝╚██████╔╝░░░░░░██████╔╝███████╗
╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚═════╝░░░░░░░╚═════╝░╚══════╝
                                Created by HengSok
    """
    banner_msg = """Example Below\nCookie: kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_dfe556cf2a8....\nUser ID: 3xnpgvvuei3umwk"""
    return banner_display, banner_msg

def main():
    
    banner_display, banner_msg = display_banner()
    tool_selector.display_banner(
        banner_display,
        banner_msg, title=" - Kuaishou"
    )
    
    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
    
    time.sleep(0.5)
    logger.info(input("Press enter to continue..."))


if __name__ == "__main__":
    main()
