import os
import sys

try:
    from downedit.site import __main__ as vid_dl
    from downedit.image.ai_gen import __main__ as gen_img_ai
    from downedit.image.ai_editor import __main__ as ai_img_editor
    from downedit.video import __main__ as video_edit
    from downedit.utils.common import DE_VERSION, tool_selector
    
    from pystyle import *
    from colorama import *
    
except ImportError as e:
    print(
        f"[Programs] [Error] {str(e)}")
    os.system("pip install -r requirements.txt")
    print(input(
        f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


def display_banner():
    banner_display = f"""{Fore.MAGENTA}
██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗░░░░░░███████╗██████╗░██╗████████╗
██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║░░░░░░██╔════╝██╔══██╗██║╚══██╔══╝
██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║█████╗█████╗░░██║░░██║██║░░░██║░░░
██║░░██║██║░░██║░░████╔═████║░██║╚████║╚════╝██╔══╝░░██║░░██║██║░░░██║░░░
██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║░░░░░░███████╗██████╔╝██║░░░██║░░░
╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝░░░░░░╚══════╝╚═════╝░╚═╝░░░╚═╝░░░
                      Created by HengSok - v{DE_VERSION}
            """
    banner_msg = "Use arrow key to select the options"
    return banner_display, banner_msg


def main():
    while True:
        tool_selector.running = True
        try:
            banner_display, banner_msg = display_banner()
            tool_selector.display_banner(banner_display, banner_msg)
            choices = [' Edit Video',
                       f' AI Edit Video {Fore.RED}(Soon)',
                       f' Edit Photo {Fore.RED}(Soon)',
                       f' AI Edit Photo',
                       ' Download Video',
                       ' AI-Generative Image',
                       f' AI-Generative Video {Fore.RED}(Soon)',
                       ' Exit']

            menu_list = {
                " Edit Video": video_edit.main,
                " AI Edit Video (Soon)": lambda: None,
                " Edit Photo (Soon)": lambda: None,
                " AI Edit Photo": ai_img_editor.main,
                " Download Video": vid_dl.main,
                " AI-Generative Image": gen_img_ai.main,
                " AI-Generative Video (Soon)": lambda: None,
                " Exit": lambda: sys.exit(0)
            }

            selected = tool_selector.select_menu(message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=choices)
            tool_selector.execute_menu(selected, menu_list)

        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
            print(input(
                f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
