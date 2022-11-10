# download all tiktok video from user
# edit video from entire directory using moviepy
# Created by HengSok


import requests,json,os,time,re
import random 
from random import choice
import inquirer
from pystyle import *
from moviepy.editor import * 
import colorama
from colorama import *
from rich.traceback import install
from rich.console import Console
from requests_html import HTMLSession
import requests_random_user_agent

install()
console = Console()
#colorama.init(autoreset=True)



def api1():
    url = "https://www.tikwm.com/api/user/posts"
    print(Box.DoubleCube(f"""Api: https://www.tikwm.com \nExample: @tiktok"""))

    KeyError = False
    while not KeyError:
        try:
            url = "https://www.tikwm.com/api/user/posts"

            querystring = {"unique_id":"", "count":"35","cursor":"0"}
            querystring["unique_id"] = input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")

            s = requests.Session()
            gen = s.headers['User-Agent']

            header = {
                "User-Agent": gen
            }

            request_data = requests.request("GET", url, headers=header, params=querystring).json()
            break         
        except:
            pass

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
        title = video['title']
        limit = str(f'{title:80.80}')
        print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[Title] {Fore.GREEN}{limit}\r""")
        # download start time                           
        start = time.time()
        # data size of each download                                        
        chunk_size = 1024

        if not os.path.exists(f"./tiktok/{username}/{title}.mp4"):

            video_bytes = requests.get(download_url, stream=True)
            total_length = int(video_bytes.headers.get("Content-Length"))
            console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
            with open(f'./tiktok/{username}/{title}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time() 

                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{uri}.mp4{Fore.YELLOW} Downloaded\n""")
                time.sleep(0.7)
            
        else:
            print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{uri}.mp4{Fore.WHITE} already exists! Skipping...\n")
            time.sleep(0.7) 
            continue
    time.sleep(1) 
    console.log(f"[cyan][Status][/cyan] Successfully downloaded [green]{count}[/green] videos ✓")

# Download All Video From Tiktok User Function
def api2():

    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/user/posts"
    print(Box.DoubleCube(f"""Api: https://tiktok-video-no-watermark2.p.rapidapi.com/ \nExample: @tiktok"""))

    key = [
        "cbb685f815msh9bb9a7c12e7952fp1c55ddjsn1313cb0b6392",
        "bc72be337fmshb7473c97adae84ep1ed443jsna2e9de2f00f5",
        "ae52c34202mshc9cc27d0dfd4288p178654jsnb7a8a5a2042f"
    ]
    api_key = random.choice(key)

    querystring = {"unique_id":"", "count":"35","cursor":"0"}
    querystring["unique_id"] = input(f"{Fore.YELLOW}Enter User:{Fore.WHITE} ")

    headers = {
        "X-RapidAPI-Key": api_key,
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
        title = video['title']
        limit = str(f'{title:80.80}')
        print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[Title] {Fore.GREEN}{limit}\r""")
        # download start time                           
        start = time.time()
        # data size of each download                                        
        chunk_size = 1024

        if not os.path.exists(f"./tiktok/{username}/{title}.mp4"):

            video_bytes = requests.get(download_url, stream=True)
            total_length = int(video_bytes.headers.get("Content-Length"))
            console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
            with open(f'./tiktok/{username}/{title}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time() 

                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{uri}.mp4{Fore.YELLOW} Downloaded\n""")
                time.sleep(0.7)
            
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
    fns = [api1, api2]
    choice(fns)()
    time.sleep(1)                   
    print(input(f"\n{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
