
import os
import time

from pystyle import *
from colorama import *


def display_banner():
    banner_display = f"""{Fore.MAGENTA} 
████████╗██╗██╗░░██╗████████╗░█████╗░██╗░░██╗░░░░░░██████╗░██╗░░░░░
╚══██╔══╝██║██║░██╔╝╚══██╔══╝██╔══██╗██║░██╔╝░░░░░░██╔══██╗██║░░░░░
░░░██║░░░██║█████═╝░░░░██║░░░██║░░██║█████═╝░█████╗██║░░██║██║░░░░░
░░░██║░░░██║██╔═██╗░░░░██║░░░██║░░██║██╔═██╗░╚════╝██║░░██║██║░░░░░
░░░██║░░░██║██║░╚██╗░░░██║░░░╚█████╔╝██║░╚██╗░░░░░░██████╔╝███████╗
░░░╚═╝░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░░░░╚═════╝░╚══════╝
                        Created by HengSok
    """
    banner_msg = "Use arrow key to select the options"
    return banner_display, banner_msg


def main():

    tikt_prnt_path = Common.ensure_or_create_directory(TIK_TOK)
    banner_display, banner_msg = display_banner()
    
    user_selection = tool_selector.site_manual_select(banner_display, banner_msg)

    if user_selection == ' Single User':
        tiktok_user = selector.single_user_select(banner_display, "Example: tiktok")
        
        if not tiktok_user: 
            logger.keybind("Press enter to continue...")
            return
        
        print(f'{Fore.GREEN}')
        dir_path = os.path.join(tikt_prnt_path, tiktok_user)
                
        user_folder = Common.ensure_or_create_directory(dir_path)

        total_videos = tt_extractor.extract_url_from_user(
        folder_path=user_folder, username=tiktok_user)

        if total_videos != 0:
            console.log(f'[cyan][File][/cyan] Downloaded [green]{total_videos}[/green] videos successfully.')
        else:
            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}No videos were processed.")
            
    elif user_selection == ' Batch Users':
        user_list = tool_selector.batch_user_select(banner_display, "Example: C:\\Users\\User\\Desktop\\tiktok_users.txt")
        
        for tiktok_user in user_list:
            print(f'{Fore.GREEN}')
            console.log(f'[cyan][Site][/cyan] User [green]{tiktok_user}[/green]')
            
            dir_path = os.path.join(tikt_prnt_path, tiktok_user)
                
            user_folder = Common.ensure_or_create_directory(dir_path)
            
            total_videos = tt_extractor.extract_url_from_user(
                folder_path=user_folder, username=tiktok_user)

            if total_videos != 0:
                console.log(f'[cyan][File][/cyan] Downloaded [green]{total_videos}[/green] videos successfully.')
            else:
                print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}No videos were processed.")

    time.sleep(0.5)
    print(input(
        f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
