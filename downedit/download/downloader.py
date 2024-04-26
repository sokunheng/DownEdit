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
from ..utils.file import FileUtil, _current_time
from ..utils.constants import CHUNK_SIZE

logger = Logger("Programs")

class Downloader:
    
    @staticmethod
    def create_dl(
        self,
        file_type: str, 
        url: str,
        file_path: str
    ):
        if file_type.lower() == "video":
            return VideoDL(url, file_path)
        elif file_type.lower() == "image":
            return ImageDL(url, file_path)
        else:
            raise ValueError("Invalid file type")

class Download(ABC):
    
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path
    
    def _get_file_info(self):
        file_bytes = requests.get(self.url, stream=True)
        try:
            total_length = int(file_bytes.headers.get("Content-Length"))
        except:
            total_length = None
        return file_bytes, total_length

    @abstractmethod
    def _start(self):
        pass


class VideoDL(Download):
    """
    Class for downloading video files.
    """
                
    def _start(self):
        """
        Starts the download process and provides feedback.
        """
        size = 0
        file_bytes, total_length = self._get_file_info()
        
        logger.info(f"File size: {size:.4f} MB".format(size=total_length / CHUNK_SIZE / 1024))
        
        FileUtil.write_file(self.file_path, file_bytes, size, total_length)


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
        file_path = FileUtil.check_file(folder_path, file_name, file_extension)

        if not file_path:
            return
        
        start_time = time.time()
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
        return 


class ImageDL(Download):
    """
    Class for downloading image files.
    """
    
    def _start(self):
        """
        Starts the download process and provides feedback.
        """
        size = 0
        file_bytes, total_length = self._get_file_info()

        FileUtil.write_file(self.file_path, file_bytes, size, total_length)

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
        file_path = FileUtil.check_file(folder_path, file_name, file_extension)
        
        if not file_path:
            return
        
        self._start()

        logger.time(
            time=_current_time(),
            info="File",
            message=f"{Fore.GREEN}{file_name}{file_extension}{Fore.YELLOW} Downloaded"
        )

        time.sleep(0.2)