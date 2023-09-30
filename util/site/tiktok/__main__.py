
import os
import time

from pystyle import *
from colorama import *
from util.common import *
from .extractor import TikTokExtractor as tt_extractor


def display_banner():
    banner = f"""{Fore.MAGENTA} 
████████╗██╗██╗░░██╗████████╗░█████╗░██╗░░██╗░░░░░░██████╗░██╗░░░░░
╚══██╔══╝██║██║░██╔╝╚══██╔══╝██╔══██╗██║░██╔╝░░░░░░██╔══██╗██║░░░░░
░░░██║░░░██║█████═╝░░░░██║░░░██║░░██║█████═╝░█████╗██║░░██║██║░░░░░
░░░██║░░░██║██╔═██╗░░░░██║░░░██║░░██║██╔═██╗░╚════╝██║░░██║██║░░░░░
░░░██║░░░██║██║░╚██╗░░░██║░░░╚█████╔╝██║░╚██╗░░░░░░██████╔╝███████╗
░░░╚═╝░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░░░░╚═════╝░╚══════╝
                        Created by HengSok
    """
    print(Center.XCenter(banner))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube(f"Example: tiktok"))


def main():

    tikt_prnt_path = Common.ensure_or_create_directory(TIK_TOK)
    os.system('cls')
    display_banner()
    tiktok_user = input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")
    
    if tiktok_user is None:
        print(
            f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Please Enter User Name!")
        
    print(f'{Fore.GREEN}')
    dir_path = os.path.join(tikt_prnt_path, tiktok_user)
    
    user_folder = Common.ensure_or_create_directory(dir_path)
    
    total_videos = tt_extractor.extract_url_from_user(
        folder_path=user_folder, username=tiktok_user)

    if total_videos != 0:
        console.log(
            f'[cyan][File][/cyan] Downloaded [green]{total_videos}[/green] videos successfully.')
    else:
        print(
            f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}No videos were processed.")

    time.sleep(0.5)
    print(input(
        f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
