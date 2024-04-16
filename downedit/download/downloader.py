import os
import re
import time
import requests

from colorama import *
from datetime import datetime
from typing import Optional, Union
from abc import ABC, abstractmethod

from ..utils.common import *
from ..utils.logger import Logger


logger = Logger("Programs")
CHUNK_SIZE = 1024


def _current_time():
    return datetime.now().strftime("%H:%M:%S")

def _normalize_filename(
    folder_location: str,
    file_name: str,
    file_extension: str
) -> str:
    cleaned_name = re.sub(r'["*<>?\\|/:]', '', file_name)
    
    dir_path = os.path.join(
        folder_location,
        cleaned_name + file_extension
    )
    
    if cleaned_name == "" or cleaned_name.isspace():
        counter = 1
        while True:
            final_name = f"{cleaned_name}{counter}{file_extension}"
            dir_path = os.path.join(folder_location, final_name)
            if not os.path.exists(dir_path):
                return dir_path
            counter += 1
            
    return dir_path

def _check_file(
    folder_path: str, 
    file_name: str, 
    file_extension: str
) -> Union[str, bool]:
        
    limit_title = file_name[:80]
    
    logger.time(
        time=_current_time(),
        info="Title",
        message=f"{Fore.GREEN}{limit_title}\r"
    )
    
    file_path = _normalize_filename(
        folder_path,
        file_name, 
        file_extension
    )
    
    if not os.path.exists(file_path):
        return file_path
    elif os.path.exists(file_path):
        logger.file_error(f"{Fore.GREEN}{file_name}{file_extension}{Fore.WHITE} already exists! Skipping...")
        time.sleep(0.3)
        return False
    else:
        logger.file_error("Invalid file! Skipping...")
        time.sleep(0.3)
        return False

def _write_file(
    file_path,
    file_bytes,
    size_default=0,
    total_length=Optional[int]
):                
    with open(file_path, 'wb') as out_file:
        for data in file_bytes.iter_content(chunk_size=CHUNK_SIZE):
            size_default += len(data)
            print('\r' +
                    f"{Fore.CYAN}[Programs] {Fore.GREEN}[Download]{Fore.WHITE} " + '%s %.2f%%' %
                    ('>' * int(size_default * 50 / total_length), float(size_default / total_length * 100)), end=' ')
            out_file.write(data)
            
    
class Download(ABC):
    
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path
    
    @abstractmethod
    def _get_file_info(self):
        pass

    @abstractmethod
    def _start(self):
        pass

        
class VideoDL(Download):
    """
    Class for downloading video files.
    """
    
    def _get_file_info(self):
        file_bytes = requests.get(self.url, stream=True)
        try:
            total_length = int(file_bytes.headers.get("Content-Length"))
        except:
            total_length = None
        return file_bytes, total_length
                
    def _start(self):
        """
        Starts the download process and provides feedback.
        """
        size = 0
        file_bytes, total_length = self._get_file_info()
        
        logger.info(f"File size: {size:.4f} MB".format(size=total_length / CHUNK_SIZE / 1024))
        
        _write_file(self.file_path, file_bytes, size, total_length)

    
    def download(
        self,
        file_name: str,
        folder_path: str,
        file_extension=".mp4"
    ):
        """
        Downloads the video file and provides feedback.
        
        - folder_path: The folder path where the file will be saved.
        - file_name: The name of the file.
        - file_extension: The extension of the file.
        """
        file_path = _check_file(folder_path, file_name, file_extension)
        start_time = time.time()
        
        if not file_path:
            return
        
        self._start()
        end_time = time.time()
        
        logger.info(
            f"Timelapse:{Fore.YELLOW}" + " %.2fs" % (end_time - start_time)
        )
        logger.time(
            time=_current_time(),
            info="File",
            message=f"{Fore.GREEN}{file_name}{file_extension}{Fore.YELLOW} Downloaded"
        )

        time.sleep(0.2)


class ImageDL(Download):
    """
    Class for downloading image files.
    """
    
    def _get_file_info(self):
        file_bytes = requests.get(self.url, stream=True)
        try:
            total_length = int(file_bytes.headers.get("Content-Length"))
        except:
            total_length = None
        return file_bytes, total_length
    
    def _start(self):
        """
        Starts the download process and provides feedback.
        
        - show_request_size: Shows the size of the file requested if true.
        - show_file_size: Shows the size of the file downloaded.
        """
        size = 0
        file_bytes, total_length = self._get_file_info()

        _write_file(self.file_path, file_bytes, size, total_length)

        f_length = os.path.getsize(self.file_path)
        f_size = f_length / (1024 ** 2)
        logger.info(f"File size: {f_size:.3f} MB")
    
    def download(
        self,
        file_name: str,
        folder_path: str,
        file_extension=".jpg"
    ):
        """
        Downloads the image file.
        
        - folder_path: The folder path where the file will be saved.
        - file_name: The name of the file.
        - file_extension: The extension of the file.
        """
        file_path = _check_file(folder_path, file_name, file_extension)
        
        if not file_path:
            return
        
        self._start()

        logger.time(
            time=_current_time(),
            info="File",
            message=f"{Fore.GREEN}{file_name}{file_extension}{Fore.YELLOW} Downloaded"
        )

        time.sleep(0.2)