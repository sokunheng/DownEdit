import os
import time


from pystyle import *
from colorama import *
from downedit.utils.common import *
from ...utils.image.image_process import *
from pathlib import Path

def check_model():
            
    dir_path = os.path.join(".")
    abs_path = os.path.abspath(dir_path)
    model_path = os.path.join(os.path.dirname(abs_path), abs_path, 'downedit', 'ml')

    model_name = 'de_net'
    file_id = '1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ'
    filename = 'de_net.pth'
    model_dir = os.path.join(model_path, 'models', 'pre_trained', filename)

    if not os.path.isfile(model_dir):
        print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.RED}Model Not found, {Fore.WHITE}downloading...""")
        download._file(folder_path=os.path.join(model_path, 'models', 'pre_trained'), 
                    download_url="https://fastupload.io/BIj6P09R1oP2/r0iY5YaYLH0gNHo/l76mZnP12manY/de_net.pth",
                    file_name=model_name,
                    file_extension=".pth")
    return model_dir

def rm_background(image_folder, output_folder=None):
    try:  
        check_ml_dir = check_model()
         
        file_folder = os.listdir(image_folder)
        file_list = ai_img_editor.get_img_list(file_folder)
        
        if not file_list:
            console.log(
                f'[cyan][File][/cyan] Processed [green]{len(file_list)}[/green] photos.')
            time.sleep(0.5)
            print(
                input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
            return

        with console.status('[cyan]Processing... please wait!', spinner='line') as status:

            for file in file_list:
                image_filename = Path(file).stem
                input_path = os.path.join(image_folder, file)

                RenderImage._remove_bg(model_dir = check_ml_dir, input_imag_path=input_path, img_name=image_filename,
                                       img_extension="_rm_bg.png", output_imag_path=output_folder)
        time.sleep(0.2)
        console.log(f'[cyan][File][/cyan] Processed [green]{len(file_list)}[/green] photos successfully.')
        time.sleep(0.3)
        print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
        
    except ImportError as e:
        print(f"[AI-Editor] [Error] {str(e)}")


def display_banner():
    banner_display = f"""{Fore.MAGENTA}
░█████╗░██╗░░░░░░███████╗██████╗░██╗████████╗░█████╗░██████╗░
██╔══██╗██║░░░░░░██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗██╔══██╗
███████║██║█████╗█████╗░░██║░░██║██║░░░██║░░░██║░░██║██████╔╝
██╔══██║██║╚════╝██╔══╝░░██║░░██║██║░░░██║░░░██║░░██║██╔══██╗
██║░░██║██║░░░░░░███████╗██████╔╝██║░░░██║░░░╚█████╔╝██║░░██║
╚═╝░░╚═╝╚═╝░░░░░░╚══════╝╚═════╝░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
                Created by HengSok - v{DE_VERSION}
    """
    banner_msg = "Select tool to edit images"
    return banner_display, banner_msg


def main():
    while tool_selector.running:
        banner_display, banner_msg = display_banner()
        tool_selector.display_banner(banner_display, banner_msg, "- ai editor")

        choices = [" Remove Background", " Back"]
        selected_tool = tool_selector.select_menu(message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}",
                                                  choices=choices)

        if selected_tool == " Remove Background":
            
            images_folder = input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
            print()

            if not os.path.exists(images_folder):
                console.log("[red][Folder][/red] No such directory")
                time.sleep(0.5)
                print(input(
                    f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
                continue

            output_folder = Common.ensure_or_create_directory(
                directory_name=os.path.join(".", AI_EDITOR))
            rm_background(images_folder, output_folder)
            
        elif selected_tool == " Back":
            tool_selector.running = False
            break


if __name__ == "__main__":
    main()
