import os
import sys
import platform

try:
    import wmi
    import psutil

    from pystyle import *
    from colorama import *

    from downedit.site import __main__ as vid_dl
    from downedit.edit.image.ai_gen import __main__ as gen_img_ai
    from downedit.edit.image.ai_editor import __main__ as ai_img_editor
    from downedit.edit.image.editor import __main__ as img_editor
    from downedit.edit.video import __main__ as video_edit
    from downedit.utils.common import DE_VERSION, tool_selector
    
except ImportError as e:
    print(f"[Programs] [Error] {str(e)}")
    os.system("pip install -r requirements.txt")
    print(
        input(
            f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."
        )
    )

def get_pc_cpu():
    cpu_info = wmi.WMI().Win32_Processor()[0]
    cpu_name = cpu_info.Name
    cpu_cores = os.cpu_count()
    
    return f"{cpu_name} ({cpu_cores} cores)"

def pc_info():
    pc_os = platform.system() + " " + platform.release() + f" ({platform.architecture()[0]})"
    pc_user = platform.node()
    pc_cpu = get_pc_cpu()
    pc_ram = psutil.virtual_memory().total / (1024**3)
    gpu_info = wmi.WMI().Win32_VideoController()[0]
    pc_gpu = gpu_info.Description if gpu_info.Description else "No GPU found"

    return pc_os, pc_user, pc_cpu, pc_ram, pc_gpu

def display_banner():
    pc_os, pc_user, pc_cpu, pc_ram, pc_gpu = pc_info()

    banner_display = f"""
{Fore.MAGENTA}██████╗░███████╗{Back.RESET}  {Back.RED}{Fore.BLACK}sokunheng@GitHub - DownEdit v{DE_VERSION}{Fore.RESET}{Back.RESET}
{Fore.MAGENTA}██╔══██╗██╔════╝{Back.RESET}  {Fore.WHITE}--------------------------{Back.RESET}
{Fore.MAGENTA}██║░░██║█████╗░░{Back.RESET}  {Fore.CYAN}OS:  {Fore.YELLOW}{pc_os}, {pc_user}{Fore.RESET}
{Fore.MAGENTA}██║░░██║██╔══╝░░{Back.RESET}  {Fore.CYAN}CPU: {Fore.YELLOW}{pc_cpu}{Fore.RESET}
{Fore.MAGENTA}██████╔╝███████╗{Back.RESET}  {Fore.CYAN}RAM: {Fore.YELLOW}{pc_ram:.3f} GB{Fore.RESET}
{Fore.MAGENTA}╚═════╝░╚══════╝{Back.RESET}  {Fore.CYAN}GPU: {Fore.YELLOW}{pc_gpu}{Fore.RESET}
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
            
            choices = [
                ' Edit Video',
                f' AI Edit Video {Fore.RED}(Soon)',
                ' Edit Photo',
                ' AI Edit Photo',
                ' Download Video',
                ' AI-Generative Image',
                f' AI-Generative Video {Fore.RED}(Soon)',
                ' Exit'
            ]

            menu_list = {
                " Edit Video": video_edit.main,
                " AI Edit Video (Soon)": lambda: None,
                " Edit Photo": img_editor.main,
                " AI Edit Photo": ai_img_editor.main,
                " Download Video": vid_dl.main,
                " AI-Generative Image": gen_img_ai.main,
                " AI-Generative Video (Soon)": lambda: None,
                " Exit": lambda: sys.exit(0)
            }

            selected = tool_selector.select_menu(
                message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}",
                choices=choices
            )
            
            tool_selector.execute_menu(
                selected,
                menu_list
            )

        except Exception as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}{str(e[:80])}"
            )
            print(
                input(
                    f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."
                )
            )
            
        except KeyboardInterrupt as e:
            print(
                f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[System] {Fore.RED} Skipping the process.."
            )
        

if __name__ == "__main__":
    main()
