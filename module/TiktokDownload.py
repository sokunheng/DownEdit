# download all tiktok video from user
# edit video from entire directory using moviepy
# Created by HengSok

import os, time
import requests
import colorama
from colorama import *
from pystyle import *
from colorama import *
from rich.traceback import install
from rich.console import Console


install()
console = Console()
#colorama.init(autoreset=True)



while True:

    # Download All Video From Tiktok User Function
    def downloadAllVidsFromUser():

        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/user/posts"

        querystring = {"unique_id":"", "count":"35","cursor":"0"}
        querystring["unique_id"] = input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")

        headers = {
            "X-RapidAPI-Key": "473e4ea488mshb270611342960f0p1c3632jsn90da643acd52",
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

        request_data = requests.request("GET", url, headers=headers, params=querystring).json()
        username = request_data["data"]["videos"][0]['author']["unique_id"]

        if not os.path.exists(f"./tiktok/{username}"):
            os.makedirs(f"./tiktok/{username}")

        videos = request_data["data"]["videos"]

        print(f"""\n{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.RED}@{username} {Fore.YELLOW}Have Published {Fore.BLUE}{len(videos)} {Fore.YELLOW}Videos. Downloading them...""")
        console.log("[cyan][Status][/cyan] Already Downloaded Videos Will Be Skipped.\n")


        count = 0
        for video in videos:
            
            count += 1
            download_url = video["play"]
            uri = video["video_id"]

            # download start time                           
            start = time.time()
            # data size of each download                                        
            chunk_size = 1024

            if not os.path.exists(f"./tiktok/{username}/{uri}.mp4"):

                video_bytes = requests.get(download_url, stream=True)
                total_length = int(video_bytes.headers.get("Content-Length"))
                console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
                with open(f'./tiktok/{username}/{uri}.mp4', 'wb') as out_file:
                    out_file.write(video_bytes.content)
                    end = time.time() 

                    print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                    print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{uri}.mp4{Fore.YELLOW} Downloaded\n""")
                
            else:
                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{uri}.mp4{Fore.WHITE} already exists! Skipping...\n")
                time.sleep(0.7) 
                continue
        time.sleep(1) 
        console.log(f"[cyan][Status][/cyan] Successfully downloaded [green]{count}[/green] videos ✓")
        

    if __name__ == "__main__":

        if not os.path.exists("./tiktok"):
            os.makedirs("./tiktok")
        os.system('cls')
        banner = f"""{Fore.MAGENTA} 
    ████████╗██╗██╗░░██╗████████╗░█████╗░██╗░░██╗░░░░░░██████╗░██╗░░░░░
    ╚══██╔══╝██║██║░██╔╝╚══██╔══╝██╔══██╗██║░██╔╝░░░░░░██╔══██╗██║░░░░░
    ░░░██║░░░██║█████═╝░░░░██║░░░██║░░██║█████═╝░█████╗██║░░██║██║░░░░░
    ░░░██║░░░██║██╔═██╗░░░░██║░░░██║░░██║██╔═██╗░╚════╝██║░░██║██║░░░░░
    ░░░██║░░░██║██║░╚██╗░░░██║░░░╚█████╔╝██║░╚██╗░░░░░░██████╔╝███████╗
    ░░░╚═╝░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░░░░╚═════╝░╚══════╝
                             Created by HengSok
                    """
        print(Center.XCenter(banner))
        print(f'{Fore.GREEN}')
        print(Box.DoubleCube(r"Example: @tiktok"))
        downloadAllVidsFromUser()
        time.sleep(1)                   
        print(input(f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))