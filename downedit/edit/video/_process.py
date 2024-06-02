import os
import time

from colorama import Fore

from ..handler import Handler
from ...utils.logger import Logger
from ...utils.file_utils import FileUtil
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
        video_preset: str,
        cpu_threads: int,
        process_folder: str,
        output_folder: str,
        **kwargs
    ):
        self._tool = tool
        self._video_speed = kwargs.get("Speed", 1.0)
        self._music_path = kwargs.get("Music", None)
        self._loop_amount = kwargs.get("Loop Amount", 1)
        self._adjust_color  = {k.lower(): v for k, v in kwargs.items()}
        self._video_preset = video_preset
        self._cpu_threads = cpu_threads
        self._input_folder = process_folder
        self._output_folder = output_folder
        self.logger = Logger("Programs")
        
        # Initialize the video operations
        self._flip_edit = Flip()
        self._speed_edit = Speed(self._video_speed)
        self._add_music_edit = AddMusic(self._music_path)
        self._loop_edit = Loop(self._loop_amount)
        self._adjust_color_edit = AdjustColor(**self._adjust_color)
        
        # Initialize operations handler
        self.operations = Handler({
            " Flip Horizontal": self._flip_edit,
            " Custom Speed": self._speed_edit,
            " Loop Video": self._loop_edit,
            " Flip + Speed": [self._flip_edit, self._speed_edit],
            " Add Music": self._add_music_edit,
            " Speed + Music": [self._speed_edit, self._add_music_edit],
            " Flip + Speed + Music": [self._flip_edit, self._speed_edit, self._add_music_edit],
            " Adjust Color": self._adjust_color_edit
        })

    def process(self):
        """
        Process the video clips in the input folder.
        """
        proceed_count = 0
        start = time.time()
        for clip in self._input_folder:
            if self._process_clip(clip):
                proceed_count += 1
            else:
                continue
        end = time.time()
        
        self.logger.info(f"Processed:{Fore.YELLOW} "+ f"%.2fs" % (end - start))
        self.logger.file_info(f"Saved at [green]{self._output_folder}[/green]")
        self.logger.file_info(f"Processed [green]{proceed_count}[/green] videos successfully.")
        self.logger.keybind("Press enter to continue..")
    
            
    def _process_clip(self, clip) -> bool:
        """
        Process the video clip.
        
        Args:
            clip (str): The video clip path.
            
        Returns:
            bool: True if the video clip was processed successfully.
        """
        # Get the input filename without the extension
        file_name, file_extension, file_size = FileUtil.get_file_info(clip)
        limit_file_name = str(f'{file_name:60.60}')
        output_file_path = ""
        output_suffix = "" 
                    
        try:
            # Execute the operations and build the suffix
            video_editor = VideoEditor(clip, output_file_path)  # No output path yet
            output_suffix = self._build_and_apply_operations(video_editor, output_suffix)
                    
            # Construct the output file path with filename, suffix, and extension
            output_file_path = FileUtil.get_output_file(
                self._output_folder,
                f"{file_name}{output_suffix}",
                file_extension
            )
            
            if os.path.exists(output_file_path):
                self.logger.file_error(
                    f"Output file already exists - {limit_file_name}{output_suffix}{file_extension}"
                )
                return False
            
            self.logger.file_info(
                f"Processing: [green]{limit_file_name}[/green]"
            )
            # Set the final output path
            video_editor.output_path = output_file_path 
            # Render the video using the final output path
            video_editor.render(
                threads=self._cpu_threads, 
                preset=self._video_preset
            )
            return True
            
        except Exception as e:
            self.logger.file_error(f"Error: {e}")
            return False
        
    def _build_and_apply_operations(self, video_editor: VideoEditor, output_suffix: str):
        """
        Builds and applies the operations to the video editor.
        
        Args:
            video_editor (VideoEditor): The video editor object.
            output_suffix (str): The output suffix.
        """
        # Get the selected operation.
        video_operation = self.operations._get(self._tool)
        if isinstance(video_operation, VideoOperation):
            output_suffix = video_operation.handle(video_editor, output_suffix)
        elif isinstance(video_operation, list):
            for operation in video_operation:
                output_suffix = operation.handle(video_editor, output_suffix)
        return output_suffix