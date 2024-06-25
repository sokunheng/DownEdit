import time

from colorama import Fore

from .._banners import get_banner
from ....utils.common import tool_selector
from ....utils.logger import logger
from ....utils.file_utils import FileUtil
from ....edit.image._process import ImageProcess


def main():
    try:
        banner_display, banner_msg = get_banner("IMAGE_EDITOR")
        tool_selector.display_banner(banner_display, banner_msg, "- Photo editor")
        available_tools = ImageProcess.get_tools()
        user_folder = FileUtil.validate_folder(
            folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
        )
        selected_tool = tool_selector.select_menu(
            message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}", 
            choices=available_tools
        )
        image_params = tool_selector.get_tool_input(
            available_tools,
            selected_tool
        )
        with ImageProcess(
            tool=selected_tool,
            process_folder=user_folder,
            batch_size=5,
            **image_params
        ) as image_process:
            image_process.start()
        
    except Exception as e:
        logger.error(e)
        time.sleep(0.5)
        logger.pause()
        return

if __name__ == "__main__":
    main()