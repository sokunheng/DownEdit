import time

from colorama import Fore

from ..handler import Handler
from ...utils.logger import Logger
from ._editor import VideoEditor
from ._task import VideoTask
from ._operation import (
    Flip,
    Speed,
    AddMusic,
    Loop,
    AdjustColor
)


class VideoProcess:
    def __init__(
        self,
        tool: str,
        video_speed: float,
        music_path: str,
        video_preset: str,
        cpu_threads: int,
        process_folder: str,
        output_folder: str
    ):
        self._tool = tool
        self._video_speed = video_speed
        self._music_path = music_path
        self._video_preset = video_preset
        self._cpu_threads = cpu_threads
        self._input_folder = process_folder
        self._output_folder = output_folder
        self.logger = Logger("Programs")

    def process(self):
        flip  = Flip()
        speed = Speed(self._video_speed)
        add_music = AddMusic(self._music_path)
        loop = Loop()
        adjust_color = AdjustColor()

        operations = Handler({
            " Flip Horizontal": flip,
            " Custom Speed": speed,
            " Loop Video": loop,
            " Flip + Speed": [flip, speed],
            " Add Music": add_music,
            " Speed + Music": [speed, add_music],
            " Flip + Speed + Music": [flip, speed, add_music],
            " Adjust Color": adjust_color,
        })
        video_operation = operations._get(self._tool)
        
        start = time.time()
        proceed_count = 0
        for clip in self._input_folder:
            try:          
                video_editor = VideoEditor(
                    clip,
                    self._output_folder
                )
                task_video = VideoTask(video_editor)
                task_video.execute(
                    video_operation,
                    self._cpu_threads,
                    self._video_preset
                )
                proceed_count += 1
            except Exception as e:
                self.logger.file_error(f"Error: {e}")
                continue
        end = time.time()
        
        self.logger.info(f"Processed:{Fore.YELLOW} "+ f"%.2fs" % (end - start))
        self.logger.file_info(f"Processed [green]{proceed_count}[/green] videos successfully.")
        self.logger.info(input("Press enter to continue..."))    