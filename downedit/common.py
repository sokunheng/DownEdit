import os
import time

from colorama import *
import inquirer
from downedit.tool_selector import ToolSelector
from downedit.video.video_editor import *
from rich.traceback import install
from rich.console import Console
from pystyle import *
from downedit.video import *
from downedit.download.downloader import Download as dl

EDITED_PATH = "Edited"
TIK_TOK = "Tiktok"
DOUYIN = "Douyin"
KUAISHOU = "Kuaishou"

IMG_GEN = "AI_Art"

video_editor = VideoEditor()
install()
console = Console()
tool_selector = ToolSelector()

DE_VERSION = open('version', 'r').read().strip()

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
    
            