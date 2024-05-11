import os
import re
import time

from datetime import datetime
from typing import Optional, Union
from colorama import Fore

from .logger import Logger
from ..__config__ import (
    CHUNK_SIZE,
    EditFolder
)


logger = Logger("Programs")


def _current_time():
    return datetime.now().strftime("%H:%M:%S")

class FileUtil:
    """
    A class that provides utility functions for managing files.
    """
    def __init__(self, folder_root: str = ".") -> None:
        """
        Initializes the FileUtil object with the specified folder path.

        Args:
            folder_path (str): The base folder path for file operations.
        """
        self.folder_root = folder_root
    
    @staticmethod
    def validate_folder(folder_path: str) -> Union[str, bool]:
        """
        Validates a folder path by checking if it exists.

        Args:
            folder_path (str): The folder path to validate.

        Returns:
            Union[str, bool]:
                - str: The folder path if it exists.
                - bool: False if the folder does not exist.
        """
        if not os.path.exists(folder_path):
            logger.folder_error("No such directory!")
            time.sleep(0.5)
            logger.info(input("Press enter to continue..."))
            return False
        return folder_path
    
    @staticmethod
    def folder_path(folder_root, directory_name: str) -> Union[str, bool]:
        """
        Ensures a directory exists. If not, it creates one and returns the absolute path.
        """
        directory = directory_name.lstrip()
        try:
            dir_path = os.path.join(folder_root, directory)
            abs_path = os.path.abspath(dir_path)
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            return abs_path
        except Exception as e:
            logger.folder_error("Error Creating directory!")
            return directory
    
    @classmethod
    def create_folder(cls, folder_type: str) -> str:
        """
        Creates a folder based on the specified type and returns its absolute path.

        Args:
            folder_type (str): The type of folder to create (e.g., "EDITED_VIDEO").

        Returns:
            str: The absolute path of the created folder.
        """
        folder_root = cls().folder_root
        folder_name = getattr(EditFolder, folder_type)
        return cls.folder_path(folder_root, folder_name)
        
    def check_file(
        self,
        folder_path: str, 
        file_name: str, 
        file_extension: str
    ) -> Union[str, bool]:
        """
        Checks if a file exists with the given name and extension within the specified folder path.

        Args:
            folder_path (str): The folder path to check.
            file_name (str): The name of the file.
            file_extension (str): The extension of the file (including the dot, e.g., ".mp4", ".jpeg").

        Returns:
            Union[str, bool]:
                - str: The full file path if the file does not exist.
                - bool: False if the file already exists, indicating skipping.
        """
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
        file_path: str,
        file_bytes: bytes,
        size_default: int = 0,
        total_length: Optional[int] = 0,
    ):   
        """
        Writes a file to the specified path with progress bar visualization.

        Args:
            file_path (str): The path to write the file to.
            file_bytes (bytes): The content of the file as bytes.
            size_default (int, optional): The starting size for tracking progress (defaults to 0).
            total_length (int, optional): The total length of the file for calculating progress (optional).
        """             
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
        """
        Normalizes a filename by removing special characters and handling empty names.

        Args:
            folder_location (str): The folder location for the file.
            file_name (str): The original filename.
            file_extension (str): The extension of the file (including the dot, e.g., ".mp4", ".jpeg").

        Returns:
            str: The normalized filename with a path.
        """
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
    
    @staticmethod
    def get_file_list(
        file_list,
        extensions
    ):
        """
        This function filters a list of files and returns a new list containing only files with the specified extension.

        Args:
            file_list: A list of filenames (strings).
            extension: The extension to filter by (including the dot, e.g., ".mp4", ".jpeg").

        Returns:
            A list of filenames that have the provided extension.
        """
        filtered_files = []
        for file in os.listdir(file_list):
            if file.lower().endswith(extensions):
                filtered_files.append(file)
        return filtered_files
    
    def get_output_file(
        self,
        folder_path: str,
        file_name: str,
        file_extension: str
    ) -> str:
        """
        Returns the output file path for the processed video.

        Args:
            folder_path (str): The folder path to save the processed video.
            file_name (str): The name of the processed video.
            file_extension (str): The extension of the processed video.

        Returns:
            str: The output file path for the processed video.
        """
        return os.path.join(folder_path, f"{file_name}{file_extension}")