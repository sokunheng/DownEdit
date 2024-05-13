from pystyle import *
from colorama import *
from pathlib import Path
from typing import Dict, Any 

from ....utils.common import *
from ....edit.image.image_process import *

def process_images(image_folder, output_folder, operation: str):
    file_folder = os.listdir(image_folder)
    file_list = ai_img_editor.get_img_list(file_folder)
    render_image = RenderImage()

    file_list_check = Common.check_file_folder_exist(image_folder)
    if not file_list_check:
        return
    
    start_actions: Dict[str, Dict[str, Any]] = {
        " Flip Image": {
            'name': 'Flipping',
            'function': render_image._flip_img,
            'suffix': '_flip'
        },
        " Crop Image": {
            'name': 'Cropping',
            'function': render_image._crop_img,
            'suffix': '_crop'
        }
    }
    start_actions = start_actions.get(operation)
    if not start_actions:
        return None
    
    with console.status(f'[cyan]{start_actions["name"]} images... please wait!', spinner='line'):
        for file in file_list:
            image_filename = Path(file).stem
            img_extension = f"{start_actions['suffix']}.{Path(file).suffix}" 
            input_path = os.path.join(image_folder, file)

            try:
                start_actions['function'](
                    input_imag_path=input_path,
                    img_name=image_filename,
                    img_extension=img_extension,
                    output_folder=output_folder
                )
                print(f"{Fore.CYAN}[{datetime.now().strftime("%H:%M:%S")}] {Fore.GREEN}[File] {Fore.WHITE}{file}")
                print(f"{Fore.YELLOW}[{datetime.now().strftime("%H:%M:%S")}] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been edited.\n")
            
            except Exception as e:
                console.log(f"[red][Folder][/red] Error processing {file}: {e}")

def display_banner():
    banner_display = f"""{Fore.MAGENTA} 
██╗███╗░░░███╗░█████╗░░██████╗░███████╗  ███████╗██████╗░██╗████████╗░█████╗░██████╗░
██║████╗░████║██╔══██╗██╔════╝░██╔════╝  ██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗██╔══██╗
██║██╔████╔██║███████║██║░░██╗░█████╗░░  █████╗░░██║░░██║██║░░░██║░░░██║░░██║██████╔╝
██║██║╚██╔╝██║██╔══██║██║░░╚██╗██╔══╝░░  ██╔══╝░░██║░░██║██║░░░██║░░░██║░░██║██╔══██╗
██║██║░╚═╝░██║██║░░██║╚██████╔╝███████╗  ███████╗██████╔╝██║░░░██║░░░╚█████╔╝██║░░██║
╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚═════╝░╚══════╝  ╚══════╝╚═════╝░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                            Created by HengSok - v{DE_VERSION}
    """
    banner_msg = "Select Models to generate images"
    return banner_display, banner_msg


def main():
    output_folder = Common.ensure_or_create_directory(EDITED_IMG)
    while tool_selector.running:
        banner_display, banner_msg = display_banner()
        tool_selector.display_banner(banner_display, banner_msg, "- photo editor")
        
        choices = [" Crop Image", " Flip Image", " Back"]
        selected_tool = tool_selector.select_menu(message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=choices)  
        if selected_tool == " Back":
            break          
        input_folder = input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
        print()
        process_images(input_folder, output_folder, selected_tool)
        print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

if __name__ == "__main__":
    main()