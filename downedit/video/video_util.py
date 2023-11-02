import os
import time

from colorama import *
from rich.traceback import install
from rich.console import Console
from pystyle import *
from downedit.common import * 

class RenderVideo:
    
    def __init__(self) -> None:
        pass
    
    def process_videos(video_folder, output_folder, process_function: int, threads: int, preset, speed_factor = 1, music_path=None):

        next_folder= None
        
        file_list = os.listdir(video_folder)
        
        clip_list = video_editor.get_clip_list(file_list)
        
        if not clip_list:
            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos.')
            time.sleep(0.5)
            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
            return 
        
        with console.status('[cyan]Processing... please wait!', spinner='line') as status:
            
            next_folder = Common.get_next_video_folder(output_folder)
            
            for file in clip_list:    
    
                output = os.path.join(next_folder, f"{file[:-4]}_{process_function}.mp4")
                limit = str(f'{file:60.60}')
                
                if os.path.exists(output):
                    console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exists, skipping...')
                    return
                
                input_path = os.path.join(video_folder, file)
                
                if os.path.exists(output) == True:
                    console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exist, skip...')
                    clip_list.remove(file)
                    pass
                
                start = time.time()
                if process_function == 1:
                    video_editor.flip(input_path=input_path, 
                                      output_path=output, 
                                      threads=threads, 
                                      preset=preset)  
                elif process_function == 2:
                    video_editor.change_speed(input_path=input_path, 
                                              speed_factor=speed_factor, 
                                              output_path=output, 
                                              threads=threads, 
                                              preset=preset) 
                elif process_function == 3:
                    video_editor.flip_and_change_speed(input_path=input_path, 
                                                       speed_factor=speed_factor, 
                                                       output_path=output, 
                                                       threads=threads, 
                                                       preset=preset) 
                elif process_function == 4:
                    video_editor.add_background_music(input_path=input_path, 
                                                      music_path=music_path, 
                                                      output_path=output, 
                                                      threads=threads, 
                                                      preset=preset) 
                elif process_function == 5:
                    video_editor.change_speed_and_add_music(input_path=input_path, 
                                                            output_path=output, 
                                                            music_path=music_path, 
                                                            speed_factor=speed_factor, 
                                                            threads=threads, 
                                                            preset=preset) 
                elif process_function == 6:
                    video_editor.change_speed_add_music_and_flip(input_path=input_path, 
                                                                 output_path=output, 
                                                                 music_path=music_path, 
                                                                 speed_factor=speed_factor, 
                                                                 tthreads=threads, 
                                                                 preset=preset) 
                elif process_function == 7:
                    video_editor.color_correction(input_path=input_path, 
                                                  output_path=output, 
                                                  threads=threads, 
                                                  preset=preset) 
                end = time.time()

                console.log(f"[cyan][File][/cyan] [green]{limit}[/green]")
                print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW} "+ f"%.2fs" % (end - start))
                print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")
                
        if next_folder:
            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{next_folder}{Fore.WHITE}")
        else:
            print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Error] {Fore.RED}No videos were processed.")
        
        time.sleep(1)
        console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
        time.sleep(0.5)
        print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
