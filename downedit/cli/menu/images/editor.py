import os
import multiprocessing
import time

from colorama import Fore

from .._banners import get_banner
from ....utils.common import tool_selector
from ....utils.logger import Logger
from ....utils.file_utils import FileUtil
from ....__config__ import Extensions


logger = Logger("Programs")

def start_process(
) -> None:
    """
    """
    input_folder = FileUtil.get_file_list(
        directory=input_folder,
        extensions=Extensions.IMAGE
    )
    # Create the output folder.
    image_folder = FileUtil.create_folder(
        folder_type="EDITED_IMG"
    )
    # Get the output folder path based on the tool.
    output_folder = FileUtil.folder_path(
        folder_root=image_folder,
        directory_name=""
    )

def main():
    try:
        banner_display, banner_msg = get_banner("IMAGE_EDITOR")
        tool_selector.display_banner(banner_display, banner_msg)
        available_tools = { 
            " Flip Horizontal"      : {},
        }
        user_folder = FileUtil.validate_folder(
            folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
        )
        selected_tool = tool_selector.select_menu(
            message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}", 
            choices=available_tools
        )
        pass
        # start_process()
        
    except Exception as e:
        logger.folder_error(e)
        time.sleep(0.5)
        logger.info(input(f"{Fore.GREEN}Press enter to continue..."))
        return

if __name__ == "__main__":
    main()
