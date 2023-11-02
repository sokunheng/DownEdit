import os
import re
import time
from colorama import *
import requests
from downedit.common import *

class Download:

    @staticmethod
    def download_video(folder_path, download_url, file_name):
        
        limit_title = file_name[:80]
        print(
            f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[Title] {Fore.GREEN}{limit_title}\r""")

        start = time.time()
        chunk_size = 1024
        size = 0
        
        cleaned_name = re.sub(r'["*<>?\\|/:]', '', file_name)
        
        file_path = os.path.join(folder_path, f"{cleaned_name}.mp4")

        if not os.path.exists(file_path):
            video_bytes = requests.get(download_url, stream=True)
            total_length = int(video_bytes.headers.get("Content-Length"))
            
            console.log(f"[green][Status][/green] File size: " +
                        "{size:.2f} MB".format(size=total_length / chunk_size / 1024))
            
            with open(file_path, 'wb') as out_file:
                for data in video_bytes.iter_content(chunk_size=chunk_size):
                    size += len(data)
                    # show progress bar
                    print('\r' + f"{Fore.CYAN}[Programs] {Fore.GREEN}[Download]{Fore.WHITE} " + '%s %.2f%%' % (
                        '>' * int(size * 50 / total_length), float(size / total_length * 100)), end=' ')
                    out_file.write(data)
                end = time.time()
                print("")
                print(
                    f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}" + " %.2fs" % (end - start))
                print(
                    f"""{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{file_name}.mp4{Fore.YELLOW} Downloaded\n""")
                time.sleep(0.7)

        else:
            print(
                f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{file_name}.mp4{Fore.WHITE} already exists! Skipping...\n")
            time.sleep(0.7)
