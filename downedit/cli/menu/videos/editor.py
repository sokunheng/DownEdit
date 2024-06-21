import multiprocessing
import time

from colorama import Fore

from .._banners import get_banner
from ....utils.common import tool_selector
from ....utils.logger import logger
from ....utils.file_utils import FileUtil
from ....edit.video._process import VideoProcess


def main():
    try:
        max_cpu_cores = multiprocessing.cpu_count()
        banner_display, banner_msg = get_banner("VIDEO_EDITOR")
        tool_selector.display_banner(banner_display, banner_msg, "- Video editor")
        available_tools = VideoProcess.get_tools()
        video_presets = {
            " Ultrafast": "ultrafast",
            " Superfast": "superfast",
            " Veryfast" : "veryfast",
            " Faster"   : "faster",
            " Fast"     : "fast",
            " Medium"   : "medium",
            " Slow"     : "slow",
        }
        cpu_cores_choices = [
            str(i) for i in range(
                1,
                max_cpu_cores + 1
            )
        ]
        user_folder = FileUtil.validate_folder(
            folder_path=input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
        )
        selected_tool = tool_selector.select_menu(
            message=f"{Fore.YELLOW}Choose Tools{Fore.WHITE}", 
            choices=available_tools
        )
        video_params = tool_selector.get_tool_input(
            available_tools,
            selected_tool
        )
        selected_presets = tool_selector.select_menu(
            message=f"{Fore.YELLOW}Video Preset{Fore.WHITE}",
            choices=video_presets
        ).lower().lstrip()
        selected_threads = tool_selector.select_menu(
            message=f"{Fore.YELLOW}CPU Threads (Max: {max_cpu_cores}){Fore.WHITE}", 
            choices=cpu_cores_choices
        )
        with VideoProcess(
            tool=selected_tool,
            video_preset=selected_presets,
            cpu_threads=int(selected_threads),
            process_folder=user_folder,
            **video_params
        ) as video_process:
            video_process.start()
        
    except Exception as e:
        logger.error(e)
        time.sleep(0.5)
        logger.pause()
        return

if __name__ == "__main__":
    main()