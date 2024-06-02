import os
import multiprocessing
import time

from colorama import Fore

from .._banners import get_banner
from ....utils.common import tool_selector
from ....utils.logger import Logger
from ....utils.file_utils import FileUtil
from ....edit.video._process import VideoProcess
from ....__config__ import Extensions


logger = Logger("Programs")

def get_function_input(available_tools, tool_name):
    """
    Get the function input based on the selected tool.
    
    Args:
        available_tools (dict): The available tools.
        tool_name (str): The selected tool.
    
    Returns:
        dict: The function input for the selected tool.
    """
    
    if tool_name not in available_tools:
        raise Exception(f"Tool '{tool_name}' not found in available tools.")

    function_input = {}
    for message, function_type in available_tools[tool_name].items():
        if not isinstance(function_type, type):
            raise Exception(f"Invalid '{function_type}' for input '{message}'.")

        prompt = f"{Fore.YELLOW}Enter {message}:{Fore.WHITE} "
        function_input[message] = function_type(input(prompt))
    
    return function_input

# TODO: Implement batch thread editing for video processing.
# Allow specifying batch size (number of videos to process at once) - 1, 2, or 3.
# Loop through the input folder in batches based on the specified size.
# Create separate video_process objects for each video in the batch.
# Use threading or multiprocessing to process videos concurrently within a batch.
# Ensure proper thread synchronization to avoid race conditions during output folder creation.
def start_process(
    tool: str,
    video_speed: float,
    music_path: str,
    loop_amount: int,
    adjust_color: tuple,
    video_preset: str,
    cpu_threads: int,
    input_folder: str
) -> None:
    """
    Start the video processing based on the selected tool.
    
    Args:
        tool (str): The selected tool.
        video_speed (float): The speed factor of the video.
        music_path (str): The path to the music file.
        video_preset (str): The video preset.
        cpu_threads (int): The number of CPU threads.
        input_folder (str): The folder containing the video files.
    
    Returns:
        None
    """
    input_folder = FileUtil.get_file_list(
        directory=input_folder,
        extensions=Extensions.VIDEO
    )
    # Create the output folder.
    video_folder = FileUtil.create_folder(
        folder_type="EDITED_VIDEO"
    )
    # Get the output folder path based on the tool.
    output_folder = FileUtil.folder_path(
        folder_root=video_folder,
        directory_name=tool
    )
    
    # Process the video.
    video_process = VideoProcess(
        tool=tool,
        video_speed=video_speed,
        music_path=music_path,
        loop_amount=loop_amount,
        adjust_color=adjust_color,
        video_preset=video_preset,
        cpu_threads=cpu_threads,
        process_folder=input_folder,
        output_folder=output_folder
    )
    video_process.process()

def main():
    try:
        max_cpu_cores = multiprocessing.cpu_count()
        banner_display, banner_msg = get_banner("VIDEO_EDITOR")
        tool_selector.display_banner(banner_display, banner_msg)
        available_tools = { 
            " Flip Horizontal"      : {},
            " Custom Speed"         : {"Speed": float},
            " Loop Video"           : {"Loop Amount": int},
            " Flip + Speed"         : {"Speed": float},
            " Add Music"            : {"Music": str},
            " Speed + Music"        : {"Speed": float, "Music": str},
            " Flip + Speed + Music" : {"Speed": float, "Music": str},
            " Adjust Color"         : {"Brightness": float, "Contrast": float, "Saturation": float},
        }
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
        tool_options = get_function_input(
            available_tools,
            selected_tool
        )
        video_speed = tool_options.get(
            "Speed",
            1.0
        )
        music_path = tool_options.get(
            "Music",
            None
        )
        loop_amount = tool_options.get(
            "Loop Amount",
            1
        )
        adjust_color = tool_options.get(
            "Brightness",
            1.0
        ), tool_options.get(
            "Contrast",
            1.0
        ), tool_options.get(
            "Saturation",
            1.0
        )
        selected_presets = tool_selector.select_menu(
            message=f"{Fore.YELLOW}Video Preset{Fore.WHITE}",
            choices=video_presets
        ).lower().lstrip()
        selected_threads = tool_selector.select_menu(
            message=f"{Fore.YELLOW}CPU Threads (Max: {max_cpu_cores}){Fore.WHITE}", 
            choices=cpu_cores_choices
        )
        start_process(
            tool=selected_tool,
            video_speed=float(video_speed),
            music_path=music_path,
            loop_amount=int(loop_amount),
            adjust_color=adjust_color,
            video_preset=selected_presets,
            cpu_threads=int(selected_threads),
            input_folder=user_folder
        )
        
    except Exception as e:
        logger.folder_error(e)
        time.sleep(0.5)
        logger.info(input(f"{Fore.GREEN}Press enter to continue..."))
        return

if __name__ == "__main__":
    main()
