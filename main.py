import os
import sys

from downedit.utils.logger import Logger
from downedit.utils.system import SystemInfo

logger = Logger("Programs")
system_info = SystemInfo()
pc_info = system_info.get_pc_info()

try:
    from pystyle import *
    from colorama import *

    from downedit.site import __main__ as vid_dl
    from downedit.edit.image.ai_gen import __main__ as gen_img_ai
    from downedit.edit.image.ai_editor import __main__ as ai_img_editor
    from downedit.edit.image.editor import __main__ as img_editor
    from downedit.edit.video import __main__ as video_edit
    from downedit.utils.constants import DE_VERSION
    from downedit.utils.common import tool_selector
    
except ImportError as e:
    logger.error(str(e))
    os.system("pip install -r requirements.txt")
    logger.info(input("Press enter to continue..."))


def display_banner():
    banner_display = f"""
    {Fore.MAGENTA}██████╗░███████╗{Back.RESET}  {Back.RED}{Fore.BLACK}sokunheng@GitHub - DownEdit v{DE_VERSION}{Fore.RESET}{Back.RESET}
    {Fore.MAGENTA}██╔══██╗██╔════╝{Back.RESET}  {Fore.WHITE}--------------------------{Back.RESET}
    {Fore.MAGENTA}██║░░██║█████╗░░{Back.RESET}  {Fore.CYAN}OS:  {Fore.YELLOW}{pc_info["OS"]}, {pc_info["USER"]}{Fore.RESET}
    {Fore.MAGENTA}██║░░██║██╔══╝░░{Back.RESET}  {Fore.CYAN}CPU: {Fore.YELLOW}{pc_info["CPU"]}{Fore.RESET}
    {Fore.MAGENTA}██████╔╝███████╗{Back.RESET}  {Fore.CYAN}RAM: {Fore.YELLOW}{pc_info["RAM"]:.3f} GB{Fore.RESET}
    {Fore.MAGENTA}╚═════╝░╚══════╝{Back.RESET}  {Fore.CYAN}GPU: {Fore.YELLOW}{pc_info["GPU"]}{Fore.RESET}
    """
    banner_msg = """Use arrow key to select the options"""
    return banner_display, banner_msg


def main():
    while True:
        tool_selector.running = True
        try:
            banner_display, banner_msg = display_banner()
            tool_selector.display_banner(
                banner_display,
                banner_msg, title=" - Main Menu"
            )
            
            available_tools = {
                " Edit Video": video_edit.main,
                f" AI Edit Video {Fore.RED}(Soon)": lambda: None,
                " Edit Photo": img_editor.main,
                " AI Edit Photo": ai_img_editor.main,
                " Download Video": vid_dl.main,
                " AI-Generative Image": gen_img_ai.main,
                f" AI-Generative Video {Fore.RED}(Soon)": lambda: None,
                " Exit": lambda: sys.exit(0)
            }
            
            tool_selector.start(
                menu_options=available_tools,
                input_message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}"
            )

        except Exception as e:
            logger.error(str(e[:80]))
            logger.info(input("Press enter to continue..."))
            
        except KeyboardInterrupt as e:
            logger.info("Skipping the process..")
        

if __name__ == "__main__":
    main()
