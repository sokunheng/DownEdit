import asyncio
import os
import sys

from ..utils.logger import logger
from ..utils.system import pc_info
from ..utils.common import tool_selector

try:
    from colorama       import Fore, Back
    from .menu.media    import media        as vid_dl
    from .menu.images   import ai_generator as gen_img_ai
    from .menu.images   import ai_editor    as ai_img_editor
    from .menu.images   import editor       as image_editor
    from .menu.videos   import editor       as video_editor
    from .menu.sounds   import editor       as sound_editor
    from ..__config__   import DE_VERSION

except ImportError as e:
    logger.error(str(e))
    os.system("pip install -r requirements.txt")
    logger.pause()


def display_banner():
    banner_display = f"""
    {Fore.MAGENTA}██████╗░███████╗{Back.RESET}  {Back.RED}{Fore.BLACK}sokunheng@GitHub - DownEdit v{DE_VERSION}{Fore.RESET}{Back.RESET}
    {Fore.MAGENTA}██╔══██╗██╔════╝{Back.RESET}  {Fore.WHITE}--------------------------{Back.RESET}
    {Fore.MAGENTA}██║░░██║█████╗░░{Back.RESET}  {Fore.CYAN}OS : {Fore.YELLOW}{pc_info["OS"]}, {pc_info["USER"]}{Fore.RESET}
    {Fore.MAGENTA}██║░░██║██╔══╝░░{Back.RESET}  {Fore.CYAN}CPU: {Fore.YELLOW}{pc_info["CPU"]}{Fore.RESET}
    {Fore.MAGENTA}██████╔╝███████╗{Back.RESET}  {Fore.CYAN}RAM: {Fore.YELLOW}{pc_info["RAM"]:.3f} GB{Fore.RESET}
    {Fore.MAGENTA}╚═════╝░╚══════╝{Back.RESET}  {Fore.CYAN}GPU: {Fore.YELLOW}{pc_info["GPU"]}{Fore.RESET}
    """
    banner_msg = """Use arrow key and enter to select the options"""
    return banner_display, banner_msg

async def display_menu():
    banner_display, banner_msg = display_banner()
    tool_selector.display_banner(
        banner_display,
        banner_msg, title=" - Main Menu"
    )
    available_tools = {
        " Download Video"                       : vid_dl.main,
        " Edit Video"                           : video_editor.main,
        f" AI Edit Video {Fore.RED}(Soon)"      : lambda: None,
        " Edit Photo"                           : image_editor.main,
        " AI Edit Photo"                        : ai_img_editor.main,
        f" Edit Sound"                          : sound_editor.main,
        f" AI Edit Sound {Fore.RED}(Soon)"      : lambda: None,
        " AI-Generative Image"                  : gen_img_ai.main,
        f" AI-Generative Video {Fore.RED}(Soon)": lambda: None,
        f" AI-Generative Music {Fore.RED}(Soon)": lambda: None,
        " Exit"                                 : lambda: sys.exit(0)
    }
    return tool_selector.start(
        menu_options=available_tools,
        input_message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}"
    )

async def main():
    while True:
        tool_selector.running = True
        try:
            await display_menu()
        except Exception as e:
            logger.error(str(e)[:80])
            await logger.pause()
        except KeyboardInterrupt:
            logger.debug("Skipping the process..")

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()