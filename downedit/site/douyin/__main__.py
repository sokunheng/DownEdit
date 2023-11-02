import os
import time

from pystyle import *
from colorama import *
from rich.traceback import install
from rich.console import Console
from downedit.common import *

def display_banner():
    
    os.system('cls')
    txt = f"""{Fore.MAGENTA}
██████╗░░█████╗░██╗░░░██╗██╗░░░██╗██╗███╗░░██╗░░░░░░██████╗░██╗░░░░░
██╔══██╗██╔══██╗██║░░░██║╚██╗░██╔╝██║████╗░██║░░░░░░██╔══██╗██║░░░░░
██║░░██║██║░░██║██║░░░██║░╚████╔╝░██║██╔██╗██║█████╗██║░░██║██║░░░░░
██║░░██║██║░░██║██║░░░██║░░╚██╔╝░░██║██║╚████║╚════╝██║░░██║██║░░░░░
██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░██║██║░╚███║░░░░░░██████╔╝███████╗
╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░░░░░░╚═════╝░╚══════╝
                    Created by HengSok{Fore.GREEN}
            """
    print(Center.XCenter(txt))
    print(Box.DoubleCube(
        f"""Ex1: https://v.douyin.com/jqwLHjF/ \nEx2: https://www.douyin.com/user/MS4wLjABAAAARz7MJzxuIgUFeEBer0sy7mMIvZzac"""))

def main():
    
    display_banner()
    
    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
    time.sleep(1.5)
    console.log(
        f"[cyan][Status][/cyan] Successfully downloaded all videos :white_check_mark:")
    time.sleep(1)
    print(input(
        f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
