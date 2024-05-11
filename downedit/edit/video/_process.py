import os
import time

from colorama import Fore

from ..handler import Handler
from ...utils.logger import Logger
from ._editor import VideoEditor
from ._operation import (
    VideoOperation,
    Flip,
    Speed,
    AddMusic,
    Loop,
    AdjustColor
)


class VideoProcess:
    """
    Process the video based on the selected tool.
    """
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
        # Video operations functionalities.
        flip  = Flip()
        speed = Speed(self._video_speed)
        add_music = AddMusic(self._music_path)
        loop = Loop()
        adjust_color = AdjustColor()
        
        # Operations to be performed on the video.
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
        # Get the selected operation.
        video_operation = operations._get(self._tool)
            
        start = time.time()
        proceed_count = 0
        for clip in self._input_folder:
            # Get the input filename without the extension
            file_name = os.path.splitext(os.path.basename(clip))[0]
            file_extension = os.path.splitext(os.path.basename(clip))[1]
            output_suffix = "" 
                        
            try:
                # Execute the operations and build the suffix
                video_editor = VideoEditor(clip, None)  # No output path yet
                if isinstance(video_operation, VideoOperation):
                    output_suffix = video_operation.handle(video_editor, output_suffix)
                elif isinstance(video_operation, list):
                    for operation in video_operation:
                        output_suffix = operation.handle(video_editor, output_suffix)
                        
                # Construct the output file path with filename, suffix, and extension
                output_file_path = os.path.join(
                    self._output_folder,
                    f"{file_name}{output_suffix}{file_extension}"
                )
                video_editor.output_path = output_file_path  # Set the final output path
                # Render the video using the final output path
                video_editor.render(
                    threads=self._cpu_threads, 
                    preset=self._video_preset
                )
                proceed_count += 1
                
            except Exception as e:
                self.logger.file_error(f"Error: {e}")
                continue
        end = time.time()
        
        self.logger.info(f"Processed:{Fore.YELLOW} "+ f"%.2fs" % (end - start))
        self.logger.file_info(f"Saved at [green]{self._output_folder}[/green]")
        self.logger.file_info(f"Processed [green]{proceed_count}[/green] videos successfully.")
        self.logger.info(input("Press enter to continue..."))    