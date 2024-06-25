import asyncio
import os
import time

from colorama import Fore

from ..base import Handler
from ...__config__ import Extensions
from ...utils.logger import logger
from ...utils.observer import Observer
from ...utils.file_utils import FileUtil
from ._editor import VideoEditor
from ._task import VideoTask
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
        batch_size: int = 5,
        **kwargs
    ):
        self.video_task = VideoTask()
        self.observer = Observer()
        self.batch_size = batch_size
        self._tool = tool
        self._adjust_color = (
            kwargs.get("Brightness", 1.0),
            kwargs.get("Contrast", 1.0),
            kwargs.get("Saturation", 1.0)
        )
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
        
        # Initialize the video operations
        self._flip_edit = Flip()
        self._speed_edit = Speed(kwargs.get("Speed", 1.0))
        self._add_music_edit = AddMusic(kwargs.get("Music", None))
        self._loop_edit = Loop(kwargs.get("Loop Amount", 1))
        self._adjust_color_edit = AdjustColor(*self._adjust_color)
        
        # Initialize operations handler
        self.operations = Handler({
            " Flip Horizontal"      : self._flip_edit,
            " Custom Speed"         : self._speed_edit,
            " Loop Video"           : self._loop_edit,
            " Flip + Speed"         : [self._flip_edit, self._speed_edit],
            " Add Music"            : self._add_music_edit,
            " Speed + Music"        : [self._speed_edit, self._add_music_edit],
            " Flip + Speed + Music" : [self._flip_edit, self._speed_edit, self._add_music_edit],
            " Adjust Color"         : self._adjust_color_edit
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
        
    async def start_async(self):
        """
        Process the videos in the input folder asynchronously.
        """
        # Initialize an empty list to hold the batches
        proceed_count = 0
        start_time = time.time()
        
        # Create batches
        num_videos = len(self._input_folder)
        for start_idx in range(0, num_videos, self.batch_size):
            if self.observer.is_termination_signaled():
                break
            
            # Create a batch processing list
            end_idx = min(start_idx + self.batch_size, num_videos)
            batch = self._input_folder[start_idx:end_idx]

            # Process each video in the batch
            for video in batch:
                if self.observer.is_termination_signaled():
                    break
                if await self._process_clip(video):
                    proceed_count += 1
                else:
                    continue
            await self.video_task.execute()
            await self.video_task.close()  
            
        elapsed_time = time.time() - start_time
        
        logger.info(f"Processed: {elapsed_time:.2f} seconds.")
        logger.file(f"Saved at [green]{self._output_folder}[/green]")
        logger.file(f"Processed [green]{proceed_count}[/green] videos successfully.")
        logger.pause()
    
            
    async def _process_clip(self, clip) -> bool:
        """
        Process the video clip.
        
        Args:
            clip (str): The video clip path.
            
        Returns:
            bool: True if the video clip was processed successfully.
        """    
        try:
            # Execute the operations and build the suffix
            video_editor = VideoEditor(clip, output_file_path)  # No output path yet
            output_suffix = self._build_and_apply_operations(video_editor, "")
                    
            # Construct the output file path with filename, suffix, and extension
            file_info = FileUtil.get_file_info(clip)
            file_name, file_extension, file_size = file_info
            full_file = f"{file_name}{output_suffix}"
            output_file_path = FileUtil.get_output_file(
                self._output_folder,
                full_file,
                file_extension
            ) 
            
            # Set the final output path
            video_editor.output_path = output_file_path 
            
            # Render the video using the final output path
            await self.video_task.add_task(
                operation_function=video_editor.render(
                    threads=self._cpu_threads, 
                    preset=self._video_preset
                ),
                operation_video=(
                    output_file_path,
                    f"{file_name}{file_extension}",
                    file_size
                )
            )
            return True
            
        except Exception as e:
            logger.error(e)
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
    
    def start(self):
        """
        Process the videos in the input folder synchronously.
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(self.start_async())
        except Exception as e:
            logger.error(e) 
            
    def __enter__(self):
        """
        Set up the context for video processing.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clean up the context after video processing.
        """
        pass