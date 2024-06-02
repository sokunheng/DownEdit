import os
import time

from colorama import Fore

from ..handler import Handler
from ...__config__ import Extensions
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
        **kwargs
    ):
        self._tool = tool
        self._video_speed = kwargs.get("Speed", 1.0)
        self._music_path = kwargs.get("Music", None)
        self._loop_amount = kwargs.get("Loop Amount", 1)
        self._adjust_color  = {k.lower(): v for k, v in kwargs.items()}
        self._video_preset = video_preset
        self._cpu_threads = cpu_threads
        self._input_folder = FileUtil.get_file_list(
            directory=process_folder,
            extensions=Extensions.VIDEO
        )
        # Create the output folder.
        self._video_folder = FileUtil.create_folder(
            folder_type="EDITED_VIDEO"
        )
        # Get the output folder path based on the tool.
        self._output_folder = FileUtil.folder_path(
            folder_root=self._video_folder,
            directory_name=tool
        )
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
    
    @staticmethod
    def get_tools() -> dict:
        """
        Get the available video editing tools.
        
        Returns:
            dict: The available video editing tools.
        """
        return { 
            " Flip Horizontal"      : {},
            " Custom Speed"         : {"Speed": float},
            " Loop Video"           : {"Loop Amount": int},
            " Flip + Speed"         : {"Speed": float},
            " Add Music"            : {"Music": str},
            " Speed + Music"        : {"Speed": float, "Music": str},
            " Flip + Speed + Music" : {"Speed": float, "Music": str},
            " Adjust Color"         : {"Brightness": float, "Contrast": float, "Saturation": float},
        }
        
    # TODO: Implement batch thread editing for video processing.
    # Allow specifying batch size (number of videos to process at once) - 1, 2, or 3.
    # Loop through the input folder in batches based on the specified size.
    # Create separate video_process objects for each video in the batch.
    # Use threading or multiprocessing to process videos concurrently within a batch.
    # Ensure proper thread synchronization to avoid race conditions during output folder creation.
    def start(self):
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
            self.logger.file_error(e)
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