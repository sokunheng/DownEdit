import os
import time
from urllib.error import HTTPError
import json as JSON

from pystyle import *
from colorama import *
from downedit.utils.tool_selector import selector
from downedit.site.enterpix.enterpix_api import EnterpixAPI


def enterpix_generate(user_prompt, img_folder_path, total_amount, download_chunk=100):
    api = EnterpixAPI()

    start_gen = 0
    while total_amount > 0:
        download_amount = min(total_amount, download_chunk)
        
        try:
            ai_generative = api.search_img(user_prompt, download_amount, start_gen)
            generated_img = ai_generative.get("images", [])
            
        except HTTPError as e:
            print(f"\n{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Attempt {start_gen + 1}/{download_amount}")
            time.sleep(1)
            start_gen += 1
            continue

        except JSON.JSONDecodeError as e:
            print(f"\n{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Attempt {start_gen + 1}/{download_amount}")
            time.sleep(1)
            start_gen += 1
            continue
        
        if not generated_img:
            break

        for img in generated_img:
            img_title = img.get("id")
            download_link = img.get("compressedUrl")
                        
            image_dl = ImageDL(download_link, img_folder_path)
            image_dl.download(img_title, img_folder_path)

        start_gen += download_amount
        total_amount -= download_amount


def display_banner():
    banner_display = f"""{Fore.MAGENTA} 
███████╗███╗░░██╗████████╗███████╗██████╗░██████╗░██╗██╗░░██╗
██╔════╝████╗░██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║╚██╗██╔╝
█████╗░░██╔██╗██║░░░██║░░░█████╗░░██████╔╝██████╔╝██║░╚███╔╝░
██╔══╝░░██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██╔═══╝░██║░██╔██╗░
███████╗██║░╚███║░░░██║░░░███████╗██║░░██║██║░░░░░██║██╔╝╚██╗
╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝
                Created by HengSok - v{DE_VERSION}
    """
    banner_msg = "Type something you want to generate"
    return banner_display, banner_msg


def main():

    banner_display, banner_msg = display_banner()
    selector.display_banner(banner_display, banner_msg)
    img_gen_prnt_path = Common.ensure_or_create_directory(IMG_GEN)
    
    user_prompt = input(f"{Fore.YELLOW}Enter Prompt:{Fore.WHITE} ")
    img_amount = input(f"{Fore.YELLOW}Enter Amount (1<=1000):{Fore.WHITE} ")

    if img_amount is None or img_amount == "":
        img_amount = 1

    if int(img_amount) > 1000:
        img_amount = 1000

    if user_prompt is None or user_prompt == "":
        user_prompt = Common.generate_prompt()

    enterpix_generate(user_prompt, img_gen_prnt_path, int(img_amount))

    time.sleep(0.5)
    print(input(
        f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
