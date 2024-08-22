
import os
import time

from pystyle import *
from colorama import *

def main():
    
    banner_display, banner_msg = get_banner("KUAISHOU_DL")
    selector.display_banner(
        banner_display,
        banner_msg, title=" - Kuaishou"
    )
    
    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
    
    time.sleep(0.5)
    logger.info(input("Press enter to continue..."))


if __name__ == "__main__":
    main()
