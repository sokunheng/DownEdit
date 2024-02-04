from datetime import datetime
import os
import time

from downedit.utils.common import *
from downedit.utils.image.ml.ai_remove_bg import remove_background
from colorama import *
from rich.traceback import install
from rich.console import Console
from pystyle import *

class RenderImage:
    def __init__(self) -> None:
        pass
    
    def _remove_bg(model_dir, input_imag_path, img_name, img_extension, output_imag_path):
        
        output_path = os.path.join(
            output_imag_path, f"{img_name}{img_extension}")
        limit = str(f'{img_name:60.60}')

        
        if os.path.exists(output_path):
            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[File] {Fore.WHITE}{limit} already exists, skipping...")
            return
        
        print(f"{Fore.CYAN}[{datetime.now().strftime("%H:%M:%S")}] {Fore.GREEN}[File] {Fore.WHITE}{limit}")
        
        start = time.time()
        output_img = remove_background(model_dir=model_dir, input_imag_path=input_imag_path,
                                       output_imag_path=output_path)
        end = time.time()

        print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapsed:{Fore.YELLOW} "+ f"%.2fs" % (end - start))
        print(f"{Fore.YELLOW}[{datetime.now().strftime("%H:%M:%S")}] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")
        
        return output_img
