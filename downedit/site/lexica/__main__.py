import os
import time
from urllib.error import HTTPError
import json as JSON

from pystyle import *
from colorama import *
from downedit.utils.common import *
from downedit.utils.requests.lexica_api import LexicaAPI


def lexica_generate(user_prompt, img_folder_path, total_amount, download_chunk=200):

    api = LexicaAPI()
    start_gen = 0

    while total_amount > 0:
        
        try:
            ai_generative = api.search_img(user_prompt, start_gen)
            generated_pmpt = ai_generative.get("prompts", [])
            next_page = ai_generative.get("nextCursor")

        except HTTPError as e:
            print(f"\n{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Attempt {start_gen + 1}/{total_amount}")
            time.sleep(1)
            start_gen += 1
            continue

        except JSON.JSONDecodeError as e:
            print(f"\n{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}Attempt {start_gen + 1}/{total_amount}")
            time.sleep(1)
            start_gen += 1
            continue
        
        if not generated_pmpt:
            break

        for pmpt in generated_pmpt:
            generated_img = pmpt.get("images", [])
            if generated_img:
                for img in generated_img:
                    if total_amount > 0:
                        img_title = img.get("id")
                        download_link = "https://image.lexica.art/full_webp/" + img_title
                        download._image(folder_path=img_folder_path, download_url=download_link,
                                        file_name=img_title, file_extension=".jpg")
                        total_amount -= 1

        start_gen = next_page


def display_banner():
    banner_display = f"""{Fore.MAGENTA} 
        ██╗░░░░░███████╗██╗░░██╗██╗░█████╗░░█████╗░
        ██║░░░░░██╔════╝╚██╗██╔╝██║██╔══██╗██╔══██╗
        ██║░░░░░█████╗░░░╚███╔╝░██║██║░░╚═╝███████║
        ██║░░░░░██╔══╝░░░██╔██╗░██║██║░░██╗██╔══██║
        ███████╗███████╗██╔╝╚██╗██║╚█████╔╝██║░░██║
        ╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░╚════╝░╚═╝░░╚═╝
                Created by HengSok - v{DE_VERSION}
    """
    banner_msg = "Type something you want to generate"
    return banner_display, banner_msg


def main():

    banner_display, banner_msg = display_banner()
    tool_selector.display_banner(banner_display, banner_msg)
    img_gen_prnt_path = Common.ensure_or_create_directory(IMG_GEN)
    
    user_prompt = input(f"{Fore.YELLOW}Enter Prompt:{Fore.WHITE} ")
    img_amount = input(f"{Fore.YELLOW}Enter Amount (1<=1000):{Fore.WHITE} ")

    if img_amount is None or img_amount == "":
        img_amount = 1

    if int(img_amount) > 1000:
        img_amount = 1000

    if user_prompt is None or user_prompt == "":
        user_prompt = Common.generate_prompt()

    lexica_generate(user_prompt, img_gen_prnt_path, int(img_amount))

    time.sleep(0.5)
    print(input(
        f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
