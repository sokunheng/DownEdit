import os
from pathlib import Path
import re
import time

from datetime import datetime
from typing import Optional, Union
from colorama import Fore

from .logger import log
from .. import (
    CHUNK_SIZE,
    EditFolder
)

class ResourceError(Exception):
    """
    Exception class for ResourceUtil errors
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class ResourceUtil:
    """
    A class that provides utility functions for managing files.
    """
    def __init__(self, folder_root: str = ".") -> None:
        """
        Initializes the ResourceUtil object with the specified folder path.

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
            raise ResourceError("No such directory!")
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
            raise FileError("Error Creating directory!")
    
    @classmethod
    def create_folder(cls, folder_type: str) -> str:
        """
        Creates a folder based on the specified type and returns its absolute path.

        Args:
            folder_type (str): The type of folder to create.
            - Options: "EDITED_VIDEO", "EDITED_IMG", "EDITED_SOUND", "AI_Photo_Gen", "AI_Photo_Editor"

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
        
        log.info(f"{limit_title}\r")
        
        file_path = self.normalize_filename(
            folder_path,
            file_name, 
            file_extension
        )
        
        if not os.path.exists(file_path):
            return file_path
        elif os.path.exists(file_path):
            log.critical(f"{file_name}{file_extension} already exists! Skipping...")
            time.sleep(0.3)
            return False
        else:
            log.error("Invalid file! Skipping...")
            time.sleep(0.3)
            return False
    
    @staticmethod
    def trim_filename(filename: Union[str, Path], max_length: int = 50) -> str:
        """
        Trim the filename to fit within the specified maximum length.

        Args:
            filename (str or Path): The full filename.
            max_length (int): The maximum number of characters to display.

        Returns:
            str: The trimmed filename.
        """
        filename = str(filename)
        if len(filename) <= max_length: return filename
        
        # Length for each part before/after ellipsis
        trim_length = (max_length - 3) // 2
        return f"{filename[:trim_length]}...{filename[-trim_length:]}"

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
    def get_file_info(file_path: str) -> tuple:
        """
        Returns the name and extension of a file.
        
        Args:
            file_path (str): The path to the file.
        
        Returns:
            tuple: A tuple containing the file name and extension.
        """
        if not os.path.exists(file_path):
            return None

        name = os.path.splitext(os.path.basename(file_path))[0]
        extension = os.path.splitext(os.path.basename(file_path))[1].lower()
        
        try:
            size = os.path.getsize(file_path)
        except (FileNotFoundError, PermissionError):
            size = None

        return name, extension, size
    
    @staticmethod
    def get_file_list(
        directory,
        extensions = None
    ):
        """
        This function filters a list of files and returns a new list containing only files with the specified extension.

        Args:
            directory: directory: The path to the directory to search for files (string).
            extension: The extension to filter by (including the dot, e.g., ".mp4", ".jpeg").

        Returns:
            A list of filenames that have the provided extension.
        """
        filtered_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if extensions is None or file.lower().endswith(extensions):
                    full_file_path = os.path.join(root, file)
                    filtered_files.append(full_file_path)
        return filtered_files
    
    @staticmethod
    def get_output_file(
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