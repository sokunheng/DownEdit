import os
import re
import time

from downedit.utils.common import *
from colorama import *
import requests
from datetime import datetime
from typing import Optional

class Download:
    def __init__(self) -> None:
        self.chunk_size = 1024

    def get_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        return current_time

    def clean_file_name(self, file_name):
        cleaned_name = re.sub(r'["*<>?\\|/:]', '', file_name)
        return cleaned_name
    
    def _get_file_info(self, download_url):
        file_bytes = requests.get(download_url, stream=True)
        try:
            total_length = int(file_bytes.headers.get("Content-Length"))
        except:
            total_length = None
        return file_bytes, total_length
    
    def _write_file(self, file_path, size, file_bytes, total_length: Optional[int] = 0):
        
        with open(file_path, 'wb') as out_file:
            for data in file_bytes.iter_content(chunk_size=self.chunk_size):
                size += len(data)
                print('\r' +
                      f"{Fore.CYAN}[Programs] {Fore.GREEN}[Download]{Fore.WHITE} " + '%s %.2f%%' %
                      ('>' * int(size * 50 / total_length), float(size / total_length * 100)), end=' ')
                out_file.write(data)
                
    def _start(self, download_url, file_path, show_request_size=False, show_file_size=False):
        size = 0
        file_bytes, total_length = self._get_file_info(download_url)

        if show_request_size:
            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}File size: {size:.4f} MB".format(
                size=total_length / self.chunk_size / 1024))
        
        self._write_file(file_path, size, file_bytes, total_length)
        
        if show_file_size:
            f_length = os.path.getsize(file_path)
            f_size = f_length / (1024 ** 2)
            print(f"""\n{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {
                  Fore.WHITE}File size: {f_size:.3f} MB""")

    def _check_file(self, folder_path, file_name, file_extension):
        limit_title = file_name[:80]
        print(
            f"\n{Fore.CYAN}[{self.get_time()}] {Fore.YELLOW}[Title] {Fore.GREEN}{limit_title}\r")

        cleaned_name = self.clean_file_name(file_name)
        file_path = os.path.join(
            folder_path, f"{cleaned_name}{file_extension}")

        if not os.path.exists(file_path):
            return file_path
        else:
            print(
                f"{Fore.CYAN}[Programs] {Fore.YELLOW}[File] {Fore.GREEN}{file_name}{file_extension}{Fore.WHITE} already exists! Skipping...\n")
            time.sleep(0.3)
            return False

    def _video(self, folder_path, download_url, file_name, file_extension):

        file_path = self._check_file(folder_path, file_name, file_extension)
        
        start = time.time()
        
        if file_path:
            self._start(download_url, file_path, show_request_size=True)
            end = time.time()
            print("")
            print(
                f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapse:{Fore.YELLOW}" + " %.2fs" % (end - start))
            print(
                f"""{Fore.CYAN}[{self.get_time()}] {Fore.YELLOW}[File] {Fore.GREEN}{file_name}{file_extension}{Fore.YELLOW} Downloaded\n""")
            time.sleep(0.2)

    def _image(self, folder_path, download_url, file_name, file_extension):

        file_path = self._check_file(folder_path, file_name, file_extension)

        if file_path:
            self._start(download_url, file_path, show_file_size=True)
            print(
                f"""{Fore.CYAN}[{self.get_time()}] {Fore.YELLOW}[File] {Fore.GREEN}{file_name}{file_extension}{Fore.YELLOW} Downloaded""")
            time.sleep(0.2)

    def _file(self, folder_path, download_url, file_name, file_extension):

        file_path = self._check_file(folder_path, file_name, file_extension)

        if file_path:
            self._start(download_url, file_path, show_file_size=True)
            print(
                f"""{Fore.CYAN}[{self.get_time()}] {Fore.YELLOW}[File] {Fore.GREEN}{file_name}{file_extension}{Fore.YELLOW} Downloaded""")
            time.sleep(0.2)
    