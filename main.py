# download all tiktok video from user
# download all douyin video from user
# download all kuaishou video from user
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

while True:
    try:
        
        #Edit Video Class
        class editVideo:

            #init Function
            def __init__(self):

                #Directory 
                
                clip_list = []
                #clip_list = os.listdir(file_list)
                def get_clip_list(file_list):
                    clip_list_input = []  
                    for file in file_list:
                        if file.endswith(".mp4") or file.endswith(".MP4") or file.endswith(".mkv"):
                            clip_list_input.append(file)
                    return clip_list_input

                #Edit Video Function
                def flip(input, output):

                    #print(path_name_list)
                    clip = VideoFileClip(input)
                    #audio = AudioFileClip(input)
                    clip = clip.fx(vfx.mirror_x)
                    name = clip.filename
                    clip.write_videofile(output, verbose= False, logger= None, codec='libx264', audio_codec="aac")
                    clip.close()
                    
                # change speed of video
                def speed(input, speed, output, xxx):
                    clip = VideoFileClip(input)
                    #audio = AudioFileClip(input)
                    clip = clip.fx(vfx.speedx, speed)
                    name = clip.filename
                    clip.write_videofile(output, verbose= False, logger= None, codec='libx264', audio_codec="aac", preset=xxx)
                    clip.close()
                
                # flip and speed
                def speednflip(input, speed, output, xxx):
                    clip = VideoFileClip(input)
                    #audio = AudioFileClip(input)
                    clip = clip.fx(vfx.mirror_x)
                    clip = clip.fx(vfx.speedx, speed)
                    name = clip.filename
                    clip.write_videofile(output, verbose= False, logger= None, codec='libx264', audio_codec="aac", preset=xxx)
                    clip.close()
                
                # add background music
                def addmusic(input, music, output, xxx):
                    videoclip = VideoFileClip(input)
                    clip_duration = videoclip.duration

                    audioclip = AudioFileClip(music)#.set_duration(clip_duration)
                    # new_audioclip = CompositeAudioClip([audioclip])
                    new_audioclip = afx.audio_loop(audioclip, duration=clip_duration)
                    
                    clip = videoclip.set_audio(new_audioclip)
                    
                    clip.write_videofile(output, verbose= False, logger= None, codec='libx264', audio_codec="aac", preset=xxx)
                    clip.close()
                
                # change speed of video and add background-music
                def musicnspeed(input, music, speed, output, xxx):
                    videoclip = VideoFileClip(input)
                    clip_duration = videoclip.duration

                    final_duration = clip_duration / speed

                    audioclip = AudioFileClip(music)#.set_duration(final_duration)
                    # new_audioclip = CompositeAudioClip([audioclip])
                    new_audioclip = afx.audio_loop(audioclip, duration=final_duration)

                    clipf = videoclip.fx(vfx.speedx, speed)
                    clip = clipf.set_audio(new_audioclip)

                    clip.write_videofile(output, verbose= False, logger= None, codec='libx264', audio_codec="aac", preset=xxx)
                    clip.close()
                
                # change speed of video, add background-music and flip video    
                def musicnspeednflip(input, music, speed, output, xxx):
                    videoclip = VideoFileClip(input)
                    clip_duration = videoclip.duration

                    final_duration = clip_duration / speed

                    audioclip = AudioFileClip(music)#.set_duration(final_duration)
                    # new_audioclip = CompositeAudioClip([audioclip])
                    new_audioclip = afx.audio_loop(audioclip, duration=final_duration)
                    
                    flipx = videoclip.fx(vfx.mirror_x)
                    clipf = flipx.fx(vfx.speedx, speed)
                    clip = clipf.set_audio(new_audioclip)

                    clip.write_videofile(output, verbose= False, logger= None, codec='libx264', audio_codec="aac", preset=xxx)
                    clip.close()
                
                #Main 
                if __name__ == "__main__":
                    if not os.path.exists("./edited/"):
                        os.makedirs("./edited")
                    if not os.path.exists("./edited/flip"):
                        os.makedirs("./edited/flip")
                    if not os.path.exists("./edited/speed"):
                        os.makedirs("./edited/speed")
                    if not os.path.exists("./edited/flip_speed"):
                        os.makedirs("./edited/flip_speed")
                    if not os.path.exists("./edited/add_music"):
                        os.makedirs("./edited/add_music")
                    if not os.path.exists("./edited/music_speed"):
                        os.makedirs("./edited/music_speed")
                    if not os.path.exists("./edited/flip_speed_music"):
                        os.makedirs("./edited/flip_speed_music")
  
                    os.system('cls')
                    banner = f"""{Fore.MAGENTA}
        ███████╗██████╗░██╗████████╗  ██╗░░░██╗██╗██████╗░███████╗░█████╗░
        ██╔════╝██╔══██╗██║╚══██╔══╝  ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗
        █████╗░░██║░░██║██║░░░██║░░░  ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║
        ██╔══╝░░██║░░██║██║░░░██║░░░  ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║
        ███████╗██████╔╝██║░░░██║░░░  ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝
        ╚══════╝╚═════╝░╚═╝░░░╚═╝░░░  ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░
                             Created by HengSok{Fore.YELLOW}
                    """
                    print(Center.XCenter(banner))

                    try:
                        # Get input directory
                        print(f'{Fore.GREEN}')
                        print(Box.DoubleCube(r"Example: C:\Users\Name\Desktop\Folder\Video"))
                        video_folder = input(f"{Fore.YELLOW}Enter folder:{Fore.WHITE} ")
                        print()
                        #print(Box.DoubleCube("Use arrow key to select the options"))
                        questions = [inquirer.List('list', message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=[' Flip Horizontal', ' Custom Speed', ' Flip And Speed', ' Add Music', ' Speed And Music', ' Flip, Speed And Music'],),]   
                        answers = inquirer.prompt(questions)
                        
                        questions2 = [inquirer.List('list', message=f"{Fore.YELLOW}Process Speed{Fore.WHITE}", choices=[' Ultrafast', ' Superfast', ' Veryfast', ' Faster', ' Fast', ' Medium', ' Slow'],),]   
                        answers2 = inquirer.prompt(questions2)
                        
                        if answers2['list'] == ' Ultrafast':
                            xxx = 'ultrafast'
                        elif answers2['list'] == ' Superfast':
                            xxx = 'superfast'
                        elif answers2['list'] == ' Veryfast':
                            xxx = 'veryfast'
                        elif answers2['list'] == ' Faster':
                            xxx = 'faster'
                        elif answers2['list'] == ' Fast':
                            xxx = 'fast'
                        elif answers2['list'] == ' Medium':
                            xxx = 'medium'
                        elif answers2['list'] == ' Slow':
                            xxx = 'slow'
                            
                        if answers['list'] == ' Flip Horizontal':

                            # check if the folder exists or not
                            if os.path.exists(video_folder):

                                # Get input files
                                file_list = os.listdir(video_folder)
                                clip_list = get_clip_list(file_list)

                                # Number of files found
                                console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
                                time.sleep(1)
                                # Process status
                                console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
                                counter = 0

                                # status or waiting
                            
                                with console.status('[cyan]Processing... please wait!', spinner='line') as status:
                                    
                                    if not clip_list:
                                        pass
                                    else:
                                        # make a new folder with counter += 1 everytime it runs.
                                        while True:
                                            counter += 1
                                            dir = "./edited/flip/Video{}".format(counter)
                                            if os.path.isdir(dir):
                                                pass
                                            else:
                                                os.makedirs(dir)
                                                break

                                    # Process files
                                    for file in clip_list:
                                        output = dir + "/" + file[:-4] + "_edited.mp4"

                                        limit = str(f'{file:60.60}')
                                        # Check if output exists in folder. If exists then skip else process
                                        if os.path.exists(output) == True:
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                                            # function skip
                                            clip_list.remove(file)
                                        else:
                                            start = time.time()
                                            flip(video_folder + "/" + file, output, xxx)
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                                            end = time.time()
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
                            time.sleep(1)
                            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
                            time.sleep(0.5)
                            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

                        elif answers['list'] == ' Custom Speed':

                            # check if the folder exists or not
                            if os.path.exists(video_folder):

                                # Get input files
                                file_list = os.listdir(video_folder)
                                clip_list = get_clip_list(file_list)

                                speedf = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Select Speed:{Fore.WHITE} "))
                                print()

                                # Number of files found
                                console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
                                time.sleep(1)
                                # Process status
                                console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
                                counter = 0

                                # status or waiting
                            
                                with console.status('[cyan]Processing... please wait!', spinner='line') as status:
                                    
                                    if not clip_list:
                                        pass
                                    else:
                                        # make a new folder with counter += 1 everytime it runs.
                                        while True:
                                            counter += 1
                                            dir = "./edited/speed/Video{}".format(counter)
                                            if os.path.isdir(dir):
                                                pass
                                            else:
                                                os.makedirs(dir)
                                                break

                                    # Process files
                                    for file in clip_list:
                                        output = dir + "/" + file[:-4] + "_speed.mp4"
                                        limit = str(f'{file:60.60}')
                                        # Check if output exists in folder. If exists then skip else process
                                        if os.path.exists(output) == True:
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                                            # function skip
                                            clip_list.remove(file)
                                        else:
                                            start = time.time()
                                            speed(video_folder + "/" + file, speedf,  output, xxx)
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                                            end = time.time()
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
                            time.sleep(1)
                            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
                            time.sleep(0.5)
                            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

                        elif answers['list'] == ' Flip And Speed':

                            # check if the folder exists or not
                            if os.path.exists(video_folder):

                                # Get input files
                                file_list = os.listdir(video_folder)
                                clip_list = get_clip_list(file_list)

                                speedf = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Select Speed:{Fore.WHITE} "))
                                print()
                                
                                # Number of files found
                                console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
                                time.sleep(1)
                                # Process status
                                console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
                                counter = 0

                                # status or waiting
                            
                                with console.status('[cyan]Processing... please wait!', spinner='line') as status:
                                    
                                    if not clip_list:
                                        pass
                                    else:
                                        # make a new folder with counter += 1 everytime it runs.
                                        while True:
                                            counter += 1
                                            dir = "./edited/flip_speed/Video{}".format(counter)
                                            if os.path.isdir(dir):
                                                pass
                                            else:
                                                os.makedirs(dir)
                                                break

                                    # Process files
                                    for file in clip_list:
                                        output = dir + "/" + file[:-4] + "_speed_flip.mp4"
                                        limit = str(f'{file:60.60}')
                                        # Check if output exists in folder. If exists then skip else process
                                        if os.path.exists(output) == True:
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                                            # function skip
                                            clip_list.remove(file)
                                        else:
                                            start = time.time()
                                            speednflip(video_folder + "/" + file, speedf, output, xxx)
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                                            end = time.time()
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
                            time.sleep(1)
                            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
                            time.sleep(0.5)
                            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
                            
                        elif answers['list'] == ' Add Music':
                            
                            if os.path.exists(video_folder):

                                # Get input files
                                file_list = os.listdir(video_folder)
                                clip_list = get_clip_list(file_list)

                                music = input(f"{Fore.YELLOW}Enter Music:{Fore.WHITE} ")
                                print()
                                
                                # Number of files found
                                console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
                                time.sleep(1)
                                # Process status
                                console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
                                counter = 0

                                # status or waiting
                            
                                with console.status('[cyan]Processing... please wait!', spinner='line') as status:
                                    
                                    if not clip_list:
                                        pass
                                    else:
                                        # make a new folder with counter += 1 everytime it runs.
                                        while True:
                                            counter += 1
                                            dir = "./edited/add_music/Video{}".format(counter)
                                            if os.path.isdir(dir):
                                                pass
                                            else:
                                                os.makedirs(dir)
                                                break

                                    # Process files
                                    for file in clip_list:
                                        output = dir + "/" + file[:-4] + "_added_music.mp4"
                                        limit = str(f'{file:60.60}')
                                        # Check if output exists in folder. If exists then skip else process
                                        if os.path.exists(output) == True:
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                                            # function skip
                                            clip_list.remove(file)
                                        else:
                                            start = time.time()
                                            addmusic(video_folder + "/" + file, music, output, xxx)
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                                            end = time.time()
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
                            time.sleep(1)
                            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
                            time.sleep(0.5)
                            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
                            
                        elif answers['list'] == ' Speed And Music':
                            
                            if os.path.exists(video_folder):

                                # Get input files
                                file_list = os.listdir(video_folder)
                                clip_list = get_clip_list(file_list)

                                music = input(f"{Fore.YELLOW}Enter Music:{Fore.WHITE} ")
                                speedf = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Select Speed:{Fore.WHITE} "))
                                print()
                                
                                # Number of files found
                                console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
                                time.sleep(1)
                                # Process status
                                console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
                                counter = 0

                                # status or waiting
                            
                                with console.status('[cyan]Processing... please wait!', spinner='line') as status:
                                    
                                    if not clip_list:
                                        pass
                                    else:
                                        # make a new folder with counter += 1 everytime it runs.
                                        while True:
                                            counter += 1
                                            dir = "./edited/music_speed/Video{}".format(counter)
                                            if os.path.isdir(dir):
                                                pass
                                            else:
                                                os.makedirs(dir)
                                                break

                                    # Process files
                                    for file in clip_list:
                                        output = dir + "/" + file[:-4] + "_speed_music.mp4"
                                        limit = str(f'{file:60.60}')
                                        # Check if output exists in folder. If exists then skip else process
                                        if os.path.exists(output) == True:
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                                            # function skip
                                            clip_list.remove(file)
                                        else:
                                            start = time.time()
                                            musicnspeed(video_folder + "/" + file, music, speedf, output, xxx)
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                                            end = time.time()
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
                            time.sleep(1)
                            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
                            time.sleep(0.5)
                            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
                        
                        elif answers['list'] == ' Flip, Speed And Music':
                            
                            if os.path.exists(video_folder):

                                # Get input files
                                file_list = os.listdir(video_folder)
                                clip_list = get_clip_list(file_list)

                                music = input(f"{Fore.YELLOW}Enter Music:{Fore.WHITE} ")
                                speedf = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Select Speed:{Fore.WHITE} "))
                                print()
                                
                                # Number of files found
                                console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
                                time.sleep(1)
                                # Process status
                                console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
                                counter = 0

                                # status or waiting
                            
                                with console.status('[cyan]Processing... please wait!', spinner='line') as status:
                                    
                                    if not clip_list:
                                        pass
                                    else:
                                        # make a new folder with counter += 1 everytime it runs.
                                        while True:
                                            counter += 1
                                            dir = "./edited/flip_speed_music/Video{}".format(counter)
                                            if os.path.isdir(dir):
                                                pass
                                            else:
                                                os.makedirs(dir)
                                                break

                                    # Process files
                                    for file in clip_list:
                                        output = dir + "/" + file[:-4] + "_speed_music_flip.mp4"
                                        limit = str(f'{file:60.60}')
                                        # Check if output exists in folder. If exists then skip else process
                                        if os.path.exists(output) == True:
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                                            # function skip
                                            clip_list.remove(file)
                                        else:
                                            start = time.time()
                                            musicnspeednflip(video_folder + "/" + file, music, speedf, output, xxx)
                                            console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                                            end = time.time()
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

                            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
                            time.sleep(1)
                            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
                            time.sleep(0.5)
                            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue..")) 
                                    
                        else:
                            console.log("[red][Folder][/red] No such directory")
                            time.sleep(3)
                    except FileNotFoundError:
                        console.log("[red][Error][/red] Please Choose the Folder")
                        time.sleep(3)

        
        # Download Video From Douyin
        class downDouyin():
            
            def __init__(self):
                class TikTok():

                    #initialization
                    def __init__(self):
                        self.headers = {
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
                            }

                        # capture all videos
                        self.Isend = False

                        # save username 
                        self.nickname = ''
                        # Likes
                        self.like_counts = 0

                        # User unique ID
                        self.sec = ''


                    def setting(self,uid,music,count,dir,mode):

                        if uid != None:
                            if uid == None:
                                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}User cannot be empty")
                                pass
                            else:
                                self.uid = uid;self.save = dir;self.count=count;self.musicarg=music;self.mode=mode
                                self.judge_link()
                        # no command received
                        else:
                            time.sleep(1)
                        
                    # Match pasted url
                    def Find(self, string):
                        # findall() Find a string that matches a regular expression
                        url = re.findall(
                            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
                        return url

                    def replaceT(self, obj):
                        """
                        @description  : Replace text illegal characters
                        ---------
                        @param  : ojb - incoming object
                        -------
                        @Returns  : n - processed content
                        -------
                        """
                        r = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                        if type(obj) == list:
                            new = []
                            for i in obj:
                                # replace with underscore
                                retest = re.sub(r, "_", i)
                                new.append(retest)
                        elif type(obj) == str:
                            # replace with underscore
                            new = re.sub(r, "_", obj)
                        return new

                    # Determine the personal homepage api link
                    def judge_link(self):

                        # Determine the length of the chain
                        r = requests.get(url = self.Find(self.uid)[0])
                        print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Downloading many {Fore.WHITE}videos.\r")
                        # get users sec_uid
                        if '?' in r.request.path_url:
                            for one in re.finditer(r'user\/([\d\D]*)([?])', str(r.request.path_url)):
                                self.sec = one.group(1)
                        else:
                            for one in re.finditer(r'user\/([\d\D]*)', str(r.request.path_url)):
                                self.sec = one.group(1)
                        # 2022/08/24: Directly use the path_url in the request, and use user\/([\d\D]*)([?]) to filter out_sec
                        print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}User's sec_id:{Fore.GREEN} "+"%s\r" % self.sec)
                        #else:
                        #    r = requests.get(url = self.Find(self.uid)[0])
                        #    print('[hint]: download multiple videos for you! \r')
                        #    # get user sec_uid
                        #    # Because in some cases there will be a ?previous_page=app_code_link parameter in the link, in order not to affect the key result, do secondary filtering
                        #    # 2022/03/02: ? previous_page, ? enter_from parameters should not appear in user homepage links
                        #    # Original user/([\d\D]*?)([?])
                        #    # try:
                        #    #     for one in re.finditer(r'user\/([\d\D]*)([?])',str(r.url)):
                        #    #         key = one.group(1)
                        #    # except:
                        #    for one in re.finditer(r'user\/([\d\D]*)',str(r.url)):
                        #        self.sec = one.group(1)
                        #    print('[Prompt]: User's sec_id=%s\r' % self.sec)

                        # first visit page number
                        max_cursor = 0


                        # Construct first visit link
                        # Doesn't work, will be update soon
                        api_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % ( 
                                self.mode, self.sec, str(self.count), max_cursor)

                        response = requests.get(url = api_post_url, headers = self.headers)
                        html = json.loads(response.content.decode())
                        self.nickname = html['aweme_list'][0]['author']['nickname']
                        if not os.path.exists(self.save + '\\' + self.nickname):
                                os.makedirs(self.save + '\\' + self.nickname)

                        self.get_data(api_post_url, max_cursor)
                        return api_post_url,max_cursor,self.sec

                    # Get the first api data
                    def get_data(self, api_post_url, max_cursor):
                        # number of attempts
                        index = 0
                        # store api data
                        result = []
                        while result == []:
                            index += 1
                            console.log(f"[cyan][Status][/cyan] Attempt [green]{index}[/green] in progress\r".format(index))
                            time.sleep(0.3)
                            response = requests.get(
                                url = api_post_url, headers = self.headers)
                            html = json.loads(response.content.decode())
                            # with open('r.json', 'wb')as f:
                            #     f.write(response.content)
                            if self.Isend == False:
                                # next page value
                                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[User] {Fore.GREEN}",str(self.nickname),'\r')
                                max_cursor = html['max_cursor']
                                result = html['aweme_list']
                                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Capture data successfully! \r")

                                # Process the first page of video information
                                self.video_info(result, max_cursor)
                            else:
                                max_cursor = html['max_cursor']
                                self.next_data(max_cursor)
                                # self.Isend = True
                                print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}There is no data on this page, skipping... \r")

                        return result,max_cursor

                    # next page
                    def next_data(self,max_cursor):
                        # Construct the next visit link
                        api_naxt_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=RuMN1wAAJu7w0.6HdIeO2EbjDc&dytk=' % (
                            self.mode, self.sec, str(self.count), max_cursor)

                        index = 0
                        result = []

                        while self.Isend == False:
                            # Return to the home page, end
                            if max_cursor == 0:
                                self.Isend = True
                                return
                            index += 1
                            print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Pairing ", max_cursor, f"page for {index} attempt!\r".format(index))
                            time.sleep(0.3)
                            response = requests.get(url = api_naxt_post_url, headers = self.headers)
                            html = json.loads(response.content.decode())
                            if self.Isend == False:
                                # next page value
                                max_cursor = html['max_cursor']
                                result = html['aweme_list']
                                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Captured data of {max_cursor} page successfully! \r".format(max_cursor))
                                # Process next page video information
                                self.video_info(result, max_cursor)
                            else:
                                self.Isend == True
                                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Failed to capture data of {max_cursor} page! \r".format(max_cursor))
                                # sys.exit()

                    # Process video information
                    def video_info(self, result, max_cursor):
                        # author_list = [] - author info   
                        # video_list = []  - No watermark video link 
                        # aweme_id = [] - Work id        
                        # nickname = [] - author id      
                        # uri_list=[] - Unique Video ID# Cover image

                        author_list = [];video_list = [];aweme_id = [];nickname = [];uri_list=[]# dynamic_cover = []

                        for v in range(self.count):
                            try:
                                author_list.append(str(result[v]['desc']))
                                # 2022/04/22
                                # If directly from /web/api/v2/aweme/post  ~This interface takes data, then only 720p resolution
                                # if in /web/api/v2/aweme/iteminfo/  ~This interface takes the video uri
                                # splice to aweme.snssdk.com/aweme/v1/play/?video_id=xxxx&radio=1080p  ~then get 1080p clear
                                video_list.append(str(result[v]['video']['play_addr']['url_list'][0]))
                                uri_list.append(str(result[v]['video']['play_addr']['uri']))
                                aweme_id.append(str(result[v]['aweme_id']))
                                nickname.append(str(result[v]['author']['nickname']))
                                # dynamic_cover.append(str(result[v]['video']['dynamic_cover']['url_list'][0]))
                            except Exception as error:
                                # print(error)
                                pass
                        # Filter illegal characters in video copy and author names
                        print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Wait for the replacement of illegal characters in the copy!")
                        author_list = self.replaceT(author_list)
                        console.log(f"[cyan][Status][/cyan] Waiting to replace the author's illegal characters...\r \n")
                        nickname = self.replaceT(nickname)
                        self.videos_download(author_list, video_list, uri_list, aweme_id, nickname, max_cursor)
                        return self,author_list,video_list,uri_list,aweme_id,nickname,max_cursor

                    # Check if a video has already been downloaded
                    def check_info(self, nickname):
                        if nickname == []:
                            return
                        else:
                            v_info = os.listdir((self.save + '\\' + nickname))
                        return v_info

                    # video download
                    def videos_download(self, author_list, video_list, uri_list, aweme_id, nickname, max_cursor):
                        # Generate video links in 1080p resolution
                        new_video_list = [];uri_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&radio=1080p&line=0'
                        # Create and check if the download directory exists
                        try:
                            os.makedirs(self.save + '\\' + nickname[0])
                        except:
                            pass

                        v_info = self.check_info(self.nickname)

                        # self.count The value may be larger than the length of the actual api，so use len(author_list) (2022/03/22)
                        for i in range(len(author_list)):

                            # Like video sorting
                            self.like_counts += 1

                            # Get single video interface information
                            try:
                                # Official interface
                                jx_url  = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_id[i]}'    
                                js = json.loads(requests.get(
                                    url = jx_url,headers=self.headers).text)

                                creat_time = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(js['item_list'][0]['create_time']))
                            except Exception as error:
                                # print(error)
                                pass

                            # remove filename  /r/n
                            author_list[i] = ''.join(author_list[i].splitlines())
                            if len(author_list[i]) > 182:
                                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}", "The file name is too long to be intercepted")
                                author_list[i] = author_list[i][0:180]
                                console.log(f"[cyan][Status][/cyan] ", f"After interception name：[green]{0}[/green]，Length：[green]{1}[/green]".format(author_list[i], len(author_list[i])))

                            # Check if the video has been downloaded
                            try:
                                if creat_time + author_list[i] + '.mp4' in v_info:
                                    time.sleep(1)
                                    title = author_list[i]
                                    limit1 = str(f'{title:80.80}')  
                                    console.log(f"[red][File][/red] [green]{limit1}[/green] [File already exists, skipping...]") 
                                    print('\r')
                                    continue
                            except:
                                # Prevent subscript out of bounds
                                pass

                            with console.status('[cyan] Fetching data video, please wait...') as status:
                                #   try to download the video
                                try:
                                    # Generate 1080p video link
                                    new_video_list.append(uri_url % uri_list[i])     
                                    # video info      
                                    video = requests.get(video_list[i])                           
                                    t_video = requests.get(url=new_video_list[0],
                                        # video content
                                        headers=self.headers).content
                                    # download start time                           
                                    start = time.time()
                                    # Initialize downloaded size                                     
                                    size = 0     
                                    # data size of each download                                        
                                    chunk_size = 1024
                                    # Total download file size                                       
                                    content_size = int(video.headers['content-length']) 
                                    try:
                                        # Check whether the response is successful
                                        if video.status_code == 200:                        
                                            title = author_list[i]
                                            limit = str(f'{title:80.80}')                        
                                            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Video] {Fore.WHITE}" + creat_time + " " + limit)
                                            console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = content_size / chunk_size /1024))    # 开始下载，显示下载文件大小

                                            if self.mode == 'post':
                                                v_url = self.save + '\\' + nickname[i] + '\\' + creat_time + re.sub(
                                                    r'[\\/:*?"<>|\r\n] + ', "_", author_list[i]) + '.mp4'
                                            else:
                                                v_url = self.save + '\\' + self.nickname + '\\' + str(self.like_counts)+ '、' + re.sub(
                                                    r'[\\/:*?"<>|\r\n] + ', "_", author_list[i]) + '.mp4'

                                            with open(v_url,'wb') as file:                
                                                for data in video.iter_content(chunk_size = chunk_size):
                                                    size += len(data)
                                                    # show progress bar
                                                    print('\r' + f"{Fore.CYAN}[Programs] {Fore.GREEN}[Download]{Fore.WHITE} " + '%s%.2f%%' % (
                                                        '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
                                                file.write(t_video)

                                                # Download end time
                                                end = time.time() 
                                                # print download time                          
                                                print('\n' + f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Time:{Fore.YELLOW}"+ " %.2fs\n" % (end - start))
                                            
                                                new_video_list = []
                                        

                                    except Exception as error:
                                        print(f'{Fore.CYAN}[Programs] {Fore.RED}[Status]{Fore.WHITE} Error downloading video!')
                                        print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status]{Fore.WHITE}", error, '\r')

                                except Exception as error:
                                    # print(error)
                                    print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status]{Fore.WHITE}", self.count, ", skipping...\r")
                                    break
                        # Get next page information
                        self.next_data(max_cursor)
                    
                # main
                if __name__ == "__main__":
                    
                    if not os.path.exists("./douyin"):
                        os.makedirs("./douyin")
                        
                    os.system('cls')
                    txt = f"""{Fore.MAGENTA}
        ██████╗░░█████╗░██╗░░░██╗██╗░░░██╗██╗███╗░░██╗░░░░░░██████╗░██╗░░░░░
        ██╔══██╗██╔══██╗██║░░░██║╚██╗░██╔╝██║████╗░██║░░░░░░██╔══██╗██║░░░░░
        ██║░░██║██║░░██║██║░░░██║░╚████╔╝░██║██╔██╗██║█████╗██║░░██║██║░░░░░
        ██║░░██║██║░░██║██║░░░██║░░╚██╔╝░░██║██║╚████║╚════╝██║░░██║██║░░░░░
        ██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░██║██║░╚███║░░░░░░██████╔╝███████╗
        ╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░░░░░░╚═════╝░╚══════╝
                    Created by HengSok - DouyinDownload V1.2.5{Fore.GREEN}
                            """
                    print(Center.XCenter(txt))
                    # draw layout
                    print(Box.DoubleCube(f"""Ex1: https://v.douyin.com/jqwLHjF/ \nEx2: https://www.douyin.com/user/MS4wLjABAAAARz7MJzxuIgUFeEBer0sy7mMIvZzac"""))

                    # Create a new instance
                    TK = TikTok()
                    user = input(f"{Fore.YELLOW}Enter User Link:{Fore.WHITE} ")
                    music = 'no'
                    count = int(35)
                    dir = 'douyin/'
                    mode = 'post'
                    TK.setting(user,music,count,dir,mode)
                    time.sleep(1.5) 
                    console.log(f"[cyan][Status][/cyan] {Fore.WHITE}Successfully downloaded all{Fore.WHITE} videos ✓")
                    time.sleep(1)                   
                    print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
        

        class dwonTiktok:

            #init Function
            def __init__(self):

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

                        if not os.path.exists(f"./tiktok/{username}/{uri}.mp4"):

                            video_bytes = requests.get(download_url, stream=True)
                            total_length = int(video_bytes.headers.get("Content-Length"))
                            console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
                            with open(f'./tiktok/{username}/{uri}.mp4', 'wb') as out_file:
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

                        if not os.path.exists(f"./tiktok/{username}/{uri}.mp4"):

                            video_bytes = requests.get(download_url, stream=True)
                            total_length = int(video_bytes.headers.get("Content-Length"))
                            console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
                            with open(f'./tiktok/{username}/{uri}.mp4', 'wb') as out_file:
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


        # Download Video From Kuaishou
        class downKuaishou():
            
            def __init__(self):
                
                def downKuai():

                    cookie = input(f"{Fore.YELLOW}Input Your Cookie:{Fore.WHITE} ")
                    uid = input(f"{Fore.YELLOW}Enter User ID:{Fore.WHITE} ")
                    header = {
                        'content-type': 'application/json',
                        # Paste your cookies here
                        'Cookie': cookie,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
                    }
                    payload = {"operationName": "privateFeedsQuery",
                                "variables": {"principalId": uid, "pcursor": "", "count": 999},
                                "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}

                    res = requests.post("https://live.kuaishou.com/m_graphql", headers=header, json=payload, timeout=15)
                    
                    works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

                    if len(works) == 0:
                        print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status] {Fore.RED}Error connection, {Fore.WHITE}please try again!")
                        time.sleep(2.5)
                    else:
                        if not os.path.exists("./kuaishou"):
                            os.makedirs("./kuaishou")

                        # These two lines of code write the response to json for analysis
                        # with open(uid + ".json", "w") as fp:
                        #     fp.write(json.dumps(works, indent=2))

                        # Prevent the user from live broadcast, the first work is live broadcast by default, 
                        # resulting in the acquisition of information as NoneType
                        # if works[0]['id'] is None:
                        #     works.pop(0)
                        try: 
                            name = re.sub(r'[\\/:*?"<>|\r\n]+', "", works[0]['user']['name'])

                            dir = "kuaishou/" + name

                            if not os.path.exists(dir):
                                os.makedirs(dir)
                        except IndexError as e:
                            print(f"{Fore.CYAN}[Programs] {Fore.RED}[Status] {Fore.WHITE}Error:{Fore.RED}", e)
                            time.sleep(1)

                        print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Start crawling users {Fore.GREEN}{name}{Fore.WHITE}, saved in {Fore.GREEN}" + dir)
                        print(f"""\n{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.RED}@{name} {Fore.YELLOW}Have Published {Fore.BLUE}{str(len(works))} {Fore.YELLOW}videos. Downloading them...""")
                        console.log("[cyan][Status][/cyan] Already Downloaded Videos Will Be Skipped.\n")

                        # Official API
                        # clientCacheKey2 = video["id"]
                        # videourl = 'https://www.kuaishou.com/short-video/' + clientCacheKey2

                        # data = {
                        #     "operationName": "visionVideoDetail",
                        #     "variables": {
                        #         "photoId": clientCacheKey2,
                        #         "page": "detail",
                        #     },
                        #     "query": "query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      croppedPhotoUrl\n      manifest {\n        mediaType\n        businessType\n        version\n        adaptationSet {\n          id\n          duration\n          representation {\n            id\n            defaultSelect\n            backupUrl\n            codecs\n            url\n            height\n            width\n            avgBitrate\n            maxBitrate\n            m3u8Slice\n            qualityType\n            qualityLabel\n            frameRate\n            featureP2sp\n            hidden\n            disableAdaptive\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    danmakuSwitch\n    __typename\n  }\n}\n"
                        # }

                        # data = json.dumps(data)

                        # response = requests.post('https://www.kuaishou.com/graphql', headers=header, data=data)
                        # response.encoding = 'zh-CN'

                        # json_data = response.json()

                        # data_title = str(json_data['data']['visionVideoDetail']['photo']['caption']).replace("r'[\/\\\:\*\?\"\<\>\|]'",'')
                        # data_url = json_data['data']['visionVideoDetail']['photo']['photoUrl']
                        # name = json_data['data']['visionVideoDetail']['author']['name']

                        count = 0
                        for video in works:

                            if video['id'] is None:
                                print(f"""{Fore.CYAN}[Programs] {Fore.RED}[File] {Fore.RED}No video found!""")
                                time.sleep(1.7)
                                break
                            else:
                                pass
                            item = video["id"]
                            w_caption = re.sub(r"\s+", " ", video['caption'])
                            w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:39]
                            print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[Title] {Fore.GREEN}{w_name}\r""")

                            AttributeError = False
                            while not AttributeError:
                                try:
                                    url = f"https://www.videofk.com/https://www.kuaishou.com/short-video/{item}"
                                    s = requests.Session()
                                    gen = s.headers['User-Agent']
                                    header = {
                                        'User-Agent': gen
                                    }
                                    session = HTMLSession()
                                    link = session.get(url=url, headers=header)
                                    time.sleep(1)
                                    sel = '#wrap > div.body-result > div > div.video_item_body > div > div.video_info > div.video_files > div > a'
                                    get = link.html.find(sel, first=True).absolute_links
                                    break         
                                except:
                                    time.sleep(0.2)
                                    pass

                            start = time.time()
                            # Initialize downloaded size                                     
                            size = 0     
                            # data size of each download                                        
                            chunk_size = 1024

                            for download_url in get:

                                if not os.path.exists(dir + '/' + f"{str(w_caption)}.mp4"):

                                    video_bytes = requests.get(download_url, stream=True)
                                    total_length = int(video_bytes.headers.get("Content-Length"))
                                    console.log(f"[green][Status][/green] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
                                    with open(dir + '/' + f"{w_caption}.mp4", 'wb') as out_file:
                                        out_file.write(video_bytes.content)
                                        end = time.time()

                                    print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}"+ " %.2fs" % (end - start))
                                    print(f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{item}.mp4{Fore.YELLOW} {Fore.WHITE}Downloaded ✓\n""")
                                    time.sleep(1)
                                else:
                                    print(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{item}.mp4{Fore.WHITE} already exists! Skipping...\n")
                                    time.sleep(1) 
                                    continue
                            count += 1
                        time.sleep(1) 
                        console.log(f"[cyan][Status][/cyan] Successfully downloaded [green]{count}[/green] videos ✓")
                        time.sleep(0.8)
                        print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

                if __name__ == "__main__":
                    os.system('cls')
                    banner = f"""{Fore.MAGENTA} 
        ██╗░░██╗██╗░░░██╗░█████╗░██╗░██████╗██╗░░██╗░█████╗░██╗░░░██╗░░░░░░██████╗░██╗░░░░░
        ██║░██╔╝██║░░░██║██╔══██╗██║██╔════╝██║░░██║██╔══██╗██║░░░██║░░░░░░██╔══██╗██║░░░░░
        █████═╝░██║░░░██║███████║██║╚█████╗░███████║██║░░██║██║░░░██║█████╗██║░░██║██║░░░░░
        ██╔═██╗░██║░░░██║██╔══██║██║░╚═══██╗██╔══██║██║░░██║██║░░░██║╚════╝██║░░██║██║░░░░░
        ██║░╚██╗╚██████╔╝██║░░██║██║██████╔╝██║░░██║╚█████╔╝╚██████╔╝░░░░░░██████╔╝███████╗
        ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝░╚════╝░░╚═════╝░░░░░░░╚═════╝░╚══════╝
                                           by HengSok
                    """
                    print(Center.XCenter(banner))
                    print(f'{Fore.GREEN}')
                    print(Box.DoubleCube(f"""Example Below\nCookie: kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_dfe556cf2a8....\nUser ID: 3xnpgvvuei3umwk"""))
                    downKuai()



        if __name__ == "__main__":
            
            os.system("cls" if os.name == "nt" else "clear"); os.system("title MMO by @HengSok" if os.name == "nt" else "")
            txt = f"""{Fore.MAGENTA}
    ██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗░░░░░░███████╗██████╗░██╗████████╗
    ██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║░░░░░░██╔════╝██╔══██╗██║╚══██╔══╝
    ██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║█████╗█████╗░░██║░░██║██║░░░██║░░░
    ██║░░██║██║░░██║░░████╔═████║░██║╚████║╚════╝██╔══╝░░██║░░██║██║░░░██║░░░
    ██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║░░░░░░███████╗██████╔╝██║░░░██║░░░
    ╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝░░░░░░╚══════╝╚═════╝░╚═╝░░░╚═╝░░░
                           Created by HengSok - v0.3.3
                  """
            
            print(Center.XCenter(txt))
            print(f'{Fore.GREEN}')
            print(Box.DoubleCube("Use arrow key to select the options"))
            questions = [inquirer.List('list', message=f"{Fore.YELLOW}Select Tools{Fore.WHITE}", choices=[' Edit Video', ' Download Douyin Video', ' Download Tiktok Video', ' Download Kuaishou Video'],),]   
            answers = inquirer.prompt(questions)

            if answers['list'] == ' Edit Video':
                editVideo()
            elif answers['list'] == ' Download Douyin Video':
                downDouyin()
            elif answers['list'] == ' Download Tiktok Video':
                dwonTiktok()
            elif answers['list'] == ' Download Kuaishou Video':
                downKuaishou()
    except:
        console.log("[red][Error][/red] Program Interupted!")
        time.sleep(2)
    
