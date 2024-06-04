import time

from colorama import Fore

from .._banners import get_banner
from ....utils.common import tool_selector
from ....utils.logger import Logger
from ....utils.file_utils import FileUtil
from ....edit.sound._process import SoundProcess


logger = Logger("Programs")


def main():
    try:
        banner_display, banner_msg = get_banner("SOUND_EDITOR")
        tool_selector.display_banner(banner_display, banner_msg, "- Sound editor")
        available_tools = SoundProcess.get_tools()
        user_folder = FileUtil.validate_folder(
            folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
        )
        selected_tool = tool_selector.select_menu(
            message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}", 
            choices=available_tools
        )
        sound_params = tool_selector.get_tool_input(
            available_tools,
            selected_tool
        )
        sound_process = SoundProcess(
            tool=selected_tool,
            process_folder=user_folder,
            **sound_params
        )
        sound_process.start()
        
    except Exception as e:
        logger.folder_error(e)
        time.sleep(0.5)
        logger.keybind(f"{Fore.GREEN}Press enter to continue...")
        return

if __name__ == "__main__":
    main()