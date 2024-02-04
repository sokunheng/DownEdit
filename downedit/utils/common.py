import os
import random
import time

from downedit.utils.tool_selector import ToolSelector
from downedit.utils.video.video_editor import *
from downedit.utils.image.image_editor import *
from downedit.utils.image.image_process import *
from downedit.video import *
from downedit.download.downloader import Download
from rich.traceback import install
from rich.console import Console
from colorama import *
from pystyle import *

EDITED_PATH = "Edited"
TIK_TOK = "Tiktok"
DOUYIN = "Douyin"
KUAISHOU = "Kuaishou"
IMG_GEN = "AI_Art"
AI_EDITOR = "AI_Editor"
DE_VERSION = open('version', 'r').read().strip()

video_editor = VideoEditor()
ai_img_editor = ImageEditor()
install()
console = Console()
tool_selector = ToolSelector()
download = Download()

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
            console.log("[red][Folder][/red] Error Creating directory!")
            return directory_name

    def get_next_video_folder(output_folder):
        counter = 1
        while True:
            dir_path = os.path.join(output_folder, f"Video{counter}")
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
                return dir_path
            counter += 1
    
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