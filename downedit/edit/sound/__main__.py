import os
import multiprocessing
import time

from enum import Enum
from colorama import *
from pystyle import *

from ...utils.file_utils import FileUtil
from ...utils.common import (
    tool_selector,
    logger,
    DE_VERSION
)

    
def display_banner():
    banner_display = f"""{Fore.MAGENTA}
███████╗██████╗░██╗████████╗  ░██████╗░█████╗░██╗░░░██╗███╗░░██╗██████╗░
██╔════╝██╔══██╗██║╚══██╔══╝  ██╔════╝██╔══██╗██║░░░██║████╗░██║██╔══██╗
█████╗░░██║░░██║██║░░░██║░░░  ╚█████╗░██║░░██║██║░░░██║██╔██╗██║██║░░██║
██╔══╝░░██║░░██║██║░░░██║░░░  ░╚═══██╗██║░░██║██║░░░██║██║╚████║██║░░██║
███████╗██████╔╝██║░░░██║░░░  ██████╔╝╚█████╔╝╚██████╔╝██║░╚███║██████╔╝
╚══════╝╚═════╝░╚═╝░░░╚═╝░░░  ╚═════╝░░╚════╝░░╚═════╝░╚═╝░░╚══╝╚═════╝░
                Created by HengSok - v{DE_VERSION}
    """
    banner_msg = r"Example: C:\Users\Name\Desktop\Folder\Video"
    return banner_display, banner_msg


def main():
    banner_display, banner_msg = display_banner()
    tool_selector.display_banner(banner_display, banner_msg)
    user_folder = FileUtil.validate_folder(
        input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    )
    time.sleep(0.5)
    logger.info(input("Press enter to continue..."))


if __name__ == "__main__":
    main()
