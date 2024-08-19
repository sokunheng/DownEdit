import os
import random
import time

from colorama import *
from pystyle import *

from .logger import log
class Common:

    @staticmethod
    def ensure_or_create_directory(directory_name):
        """Ensures a directory exists. If not, it creates one and returns the absolute path."""
        try:
            dir_path = os.path.join(".", directory_name)
            abs_path = os.path.abspath(dir_path)
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            return abs_path
        except Exception as e:
            log.error("Error Creating directory!")
            return directory_name

    def get_next_video_folder(output_folder):
        counter = 1
        while True:
            dir_path = os.path.join(output_folder, f"Video{counter}")
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
                return dir_path
            counter += 1
            
    def check_folder_exist(folder):
        if not os.path.exists(folder):
            log.error("No such directory!")
            time.sleep(0.3)
            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
            return False
        return True
    
    def check_file_folder_exist(file_folder):
        if not file_folder:
            log.error(" No such file!")
            time.sleep(0.3)
            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))
            return False
        return True
    
    def generate_prompt():
        subjects = ['A cat', 'The sun', 'A dog',
                    'The ocean', 'The moon', 'The Earth', 'A robot']
        verbs = ['jumps', 'shines', 'laughs', 'reflects', 'dances', 'sleeps']
        adjectives = ['happy', 'bright', 'playful',
                    'mysterious', 'colorful', 'beautiful']
        objects = ['on the roof', 'on galaxy', 'in the sky',
                'at the party', 'under the moon', 'in the forest']

        sentence = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(adjectives)} {random.choice(objects)}"
        return sentence