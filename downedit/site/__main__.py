from pystyle import *
from colorama import *
from downedit.utils.common import *
from downedit.site.douyin import __main__ as douyin
from downedit.site.kuaishou import __main__ as kuaishou
from downedit.site.tiktok import __main__ as tiktok
from downedit.utils.common import DE_VERSION


def display_banner():
    banner_display = f"""{Fore.MAGENTA}
██╗░░░██╗██╗██████╗░░░░░░░██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗
██║░░░██║██║██╔══██╗░░░░░░██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║
╚██╗░██╔╝██║██║░░██║█████╗██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║
░╚████╔╝░██║██║░░██║╚════╝██║░░██║██║░░██║░░████╔═████║░██║╚████║
░░╚██╔╝░░██║██████╔╝░░░░░░██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║
░░░╚═╝░░░╚═╝╚═════╝░░░░░░░╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝
                    Created by HengSok - v{DE_VERSION}
            """
    banner_msg = "Use arrow key to select the options"
    return banner_display, banner_msg


def main():
    while tool_selector.running:
        try:
            banner_display, banner_msg = display_banner()
            tool_selector.display_banner(banner_display, banner_msg)
            questions = [' Douyin', ' Tiktok', ' Kuaishou', ' Back']

            selected = tool_selector.select_menu(
                message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=questions)\

            menu_list = {
                " Douyin": douyin.main,
                " Tiktok": tiktok.main,
                " Kuaishou": kuaishou.main,
                " Back": lambda: None
            }

            tool_selector.execute_menu(selected, menu_list)

        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}")
            print(input(
                f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
