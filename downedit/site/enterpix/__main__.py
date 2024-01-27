import os
import time

from pystyle import *
from colorama import *
from downedit.common import *
from downedit.site.enterpix.api import EnterpixAPI
import random


def download_in_chunks(user_prompt, img_folder_path, total_amount, download_chunk=100):
    api = EnterpixAPI()

    start_gen = 0
    while total_amount > 0:
        download_amount = min(total_amount, download_chunk)

        ai_generative = api.search_img(user_prompt, download_amount, start_gen)
        generated_img = ai_generative["images"]

        for img in generated_img:
            img_title = img["id"]
            download_link = img["compressedUrl"]
            dl.download_image(folder_path=img_folder_path,
                              download_url=download_link, file_name=img_title)

        start_gen += download_amount
        total_amount -= download_amount


def generate_prompt():
    subjects = ['A cat', 'The sun', 'A dog',
                'The ocean', 'The moon', 'The Earth', 'A robot']
    verbs = ['jumps', 'shines', 'laughs', 'reflects', 'dances', 'sleeps']
    adjectives = ['happy', 'bright', 'playful',
                  'mysterious', 'colorful', 'beautiful']
    objects = ['on the roof', 'on galaxy', 'in the sky',
               'at the party', 'under the moon', 'in the forest']

    sentence = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(adjectives)} {random.choice(objects)}"
    return sentence


def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    os.system("title DownEdit" if os.name == "nt" else "")
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

    img_gen_prnt_path = Common.ensure_or_create_directory(IMG_GEN)
    banner_display, banner_msg = display_banner()
    print(Center.XCenter(banner_display))
    print(f'{Fore.GREEN}')
    print(Box.DoubleCube(banner_msg))
    user_prompt = input(f"{Fore.YELLOW}Enter Prompt:{Fore.WHITE} ")
    img_amount = input(f"{Fore.YELLOW}Enter Amount (1<=1000):{Fore.WHITE} ")

    if img_amount is None or img_amount == "":
        img_amount = 1

    if int(img_amount) > 1000:
        img_amount = 1000

    if user_prompt is None or user_prompt == "":
        user_prompt = generate_prompt()

    download_in_chunks(user_prompt, img_gen_prnt_path, int(img_amount))

    time.sleep(0.5)
    print(input(
        f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))


if __name__ == "__main__":
    main()
