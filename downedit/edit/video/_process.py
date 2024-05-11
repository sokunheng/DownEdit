

import time
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
        self.tool = tool
        self.video_speed = video_speed
        self.music_path = music_path
        self.video_preset = video_preset
        self.cpu_threads = cpu_threads
        self.input_folder = process_folder
        self.output_folder = output_folder

    def process(self):
        flip  = Flip()
        speed = Speed(self.video_speed)
        add_music = AddMusic(self.music_path)
        loop = Loop()
        adjust_color = AdjustColor()

        operations = { 
            " Flip Horizontal": flip,
            " Custom Speed": speed,
            " Loop Video": loop,
            " Flip + Speed": [flip, speed],
            " Add Music": add_music,
            " Speed + Music": [speed, add_music],
            " Flip + Speed + Music": [flip, speed, add_music],
            " Adjust Color": adjust_color,
        }
        video_operation = operations.get(self.tool)

        for clip in self.input_folder:
            video_editor = VideoEditor(
                clip,
                self.output_folder
            )
            task_video = VideoTask(video_editor)
            task_video.execute(
                video_operation,
                self.cpu_threads,
                self.video_preset
            )