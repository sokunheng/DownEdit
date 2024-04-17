import os
import re
import time

from datetime import datetime
from typing import Optional, Union
from colorama import Fore

from .common import logger

CHUNK_SIZE = 1024

def _current_time():
    return datetime.now().strftime("%H:%M:%S")

class FileUtil:
    
    def __init__(self, folder_path):
        self.folder_path = folder_path
    
    def check_file(
        self,
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
        
        file_path = self.normalize_filename(
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

    def write_file(
        self,
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

    def normalize_filename(
        self,
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