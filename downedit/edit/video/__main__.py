import os
from enum import Enum
from colorama import *
from pystyle import *
from ...utils.common import *
from ...utils.video.video_process import *
import multiprocessing


class Tools(Enum):
    FLIP_HORIZONTAL = 1
    CUSTOM_SPEED = 2
    FLIP_AND_SPEED = 3
    ADD_MUSIC = 4
    SPEED_AND_MUSIC = 5
    FLIP_SPEED_MUSIC = 6


TOOL_TO_DIRECTORY = {
    Tools.FLIP_HORIZONTAL: "Flip",
    Tools.CUSTOM_SPEED: "Speed",
    Tools.FLIP_AND_SPEED: "Flip_Speed",
    Tools.ADD_MUSIC: "Add_Music",
    Tools.SPEED_AND_MUSIC: "Speed_Music",
    Tools.FLIP_SPEED_MUSIC: "Flip_Speed_Music"
}


def display_banner():
    banner_display = f"""{Fore.MAGENTA}
███████╗██████╗░██╗████████╗  ██╗░░░██╗██╗██████╗░███████╗░█████╗░
██╔════╝██╔══██╗██║╚══██╔══╝  ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗
█████╗░░██║░░██║██║░░░██║░░░  ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║
██╔══╝░░██║░░██║██║░░░██║░░░  ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║
███████╗██████╔╝██║░░░██║░░░  ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝
╚══════╝╚═════╝░╚═╝░░░╚═╝░░░  ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░
                Created by HengSok - v{DE_VERSION}
    """
    banner_msg = r"Example: C:\Users\Name\Desktop\Folder\Video"
    return banner_display, banner_msg


def get_speed_factor(tool):
    if tool in ["Custom Speed", "Flip And Speed", "Speed And Music", "Flip Speed Music"]:
        return eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Select Speed:{Fore.WHITE} "))
    return 1.0


def get_music_path(tool):
    if tool in ["Add Music", "Speed And Music", "Flip Speed Music"]:
        return input(f"{Fore.YELLOW}Enter Music:{Fore.WHITE} ")
    return None


def get_preset_from_answer(answer):

    presets_mapping = {
        ' Ultrafast': 'ultrafast',
        ' Superfast': 'superfast',
        ' Veryfast': 'veryfast',
        ' Faster': 'faster',
        ' Fast': 'fast',
        ' Medium': 'medium',
        ' Slow': 'slow',
    }
    return presets_mapping.get(answer, 'medium')


def main():

    Common.ensure_or_create_directory(EDITED_VIDEO)

    banner_display, banner_msg = display_banner()
    tool_selector.display_banner(banner_display, banner_msg)

    video_folder = input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
    print()

    if not os.path.exists(video_folder):
        console.log("[red][Folder][/red] No such directory")
        time.sleep(0.5)
        print(input(
            f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
        return

    tools_choices = [
        tool.name.replace("_", " ").title() for tool in Tools
    ]

    speed_choices = [' Ultrafast', ' Superfast', ' Veryfast', ' Faster',
                     ' Fast', ' Medium', ' Slow']

    max_cpu_cores = multiprocessing.cpu_count()
    cpu_cores_choices = [str(i) for i in range(1, max_cpu_cores + 1)]

    tool_answer = tool_selector.select_menu(
        message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=tools_choices)
    speed_answer = tool_selector.select_menu(
        message=f"{Fore.YELLOW}Process Speed{Fore.WHITE}", choices=speed_choices)
    cpu_answer = tool_selector.select_menu(
        message=f"{Fore.YELLOW}CPU Threads (Max: {max_cpu_cores}){Fore.WHITE}", choices=cpu_cores_choices)

    selected_tool = Tools[tool_answer.replace(" ", "_").upper()]

    preset = get_preset_from_answer(speed_answer)

    output_folder = Common.ensure_or_create_directory(
        directory_name=os.path.join(".", EDITED_VIDEO, TOOL_TO_DIRECTORY[selected_tool]))

    speedf = get_speed_factor(tool_answer)
    music_path = get_music_path(tool_answer)

    RenderVideo.process_videos(video_folder=video_folder, output_folder=output_folder,
                               process_function=selected_tool.value, speed_factor=speedf, music_path=music_path, threads=int(cpu_answer), preset=preset)


if __name__ == "__main__":
    main()
