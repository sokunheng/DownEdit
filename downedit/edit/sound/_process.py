import asyncio
import os
import time

from ..base import Handler
from ...__config__ import Extensions
from ...utils.logger import logger
from ...utils.observer import Observer
from ...utils.file_utils import FileUtil
from ._editor import SoundEditor
from ._task import SoundTask
from ._operation import (
    SoundOperation,
    Volume,
    FadeIn,
    FadeOut
)


class SoundProcess:
    def __init__(
        self,
        tool: str,
        process_folder: str,
        batch_size: int = 5,
        **kwargs
    ) -> None:
        self.sound_task = SoundTask()
        self.observer = Observer()
        self.batch_size = batch_size
        self._tool = tool
        self._input_folder = FileUtil.get_file_list(
            directory=process_folder,
            extensions=Extensions.SOUND
        )
        # Create the output folder.
        self._sound_folder = FileUtil.create_folder(
            folder_type="EDITED_SOUND"
        )
        # Get the output folder path based on the tool.
        self._output_folder = FileUtil.folder_path(
            folder_root=self._sound_folder,
            directory_name=tool
        )
        
        # Initialize the sound operations
        self._volume = Volume(kwargs.get("Level", 0.5))
        self._fade_in = FadeIn(kwargs.get("Fade In Duration", 2))
        self._fade_out = FadeOut(kwargs.get("Fade Out Duration", 2))
        
        # Initialize operations handler
        self.operations = Handler({
            " Volume": self._volume,
            " Fade In": self._fade_in,
            " Fade Out": self._fade_out
        })
    
    @staticmethod
    def get_tools() -> dict:
        """
        Get the available sound editing tools.
        
        Returns:
            dict: The available sound editing tools.
        """
        return { 
            " Volume": {"Level": float},
            " Fade In": {"Fade In Duration": float},
            " Fade Out": {"Fade Out Duration": float},
        }
    
    async def start_async(self):
        """
        Process the sounds in the input folder asynchronously.
        """
        # Initialize an empty list to hold the batches
        proceed_count = 0
        start_time = time.time()
        
        # Create batches
        num_sounds = len(self._input_folder)
        for start_idx in range(0, num_sounds, self.batch_size):
            if self.observer.is_termination_signaled():
                break
            
            # Create a batch processing list
            end_idx = min(start_idx + self.batch_size, num_sounds)
            batch = self._input_folder[start_idx:end_idx]

            # Process each sound in the batch
            for sound in batch:
                if self.observer.is_termination_signaled():
                    break
                if await self._process_sound(sound):
                    proceed_count += 1
                else:
                    continue
            await self.sound_task.execute()
            await self.sound_task.close()  
            
        elapsed_time = time.time() - start_time

        logger.info(f"Processed: {elapsed_time:.2f} seconds.")
        logger.file(f"Saved at [green]{self._output_folder}[/green]")
        logger.file(f"Processed [green]{proceed_count}[/green] sounds successfully.")
        logger.pause()
    
    async def _process_sound(self, sound) -> bool:
        """
        Process the sound clip.
        
        Args:
            clip (str): The sound clip path.
            
        Returns:
            bool: True if the sound clip was processed successfully.
        """
        try:
            # Execute the operations and build the suffix
            sound_editor = SoundEditor(sound)
            output_suffix = self._build_and_apply_operations(sound_editor, output_suffix)
            
            # Construct the output file path with filename, suffix, and extension
            file_info = FileUtil.get_file_info(sound)
            file_name, file_extension, file_size = file_info
            full_file = f"{file_name}{output_suffix}"
            output_file_path = FileUtil.get_output_file(
                self._output_folder,
                full_file,
                file_extension
            ) 

            # Set the final output path
            sound_editor.output_path = output_file_path

            # Save the sound
            await self.sound_task.add_task(
                operation_function=sound_editor.render(),
                operation_sound=(
                    output_file_path,
                    f"{file_name}{file_extension}",
                    file_size
                )
            )
            return True
                
        except Exception as e:
            logger.error(e)
            return False

    
    def _build_and_apply_operations(self, editor: SoundEditor, suffix: str) -> str:
        """
        Build the suffix based on the operations and apply them to the editor.
        
        Args:
            editor (soundEditor): The sound editor.
            suffix (str): The current suffix.
            
        Returns:
            str: The updated suffix.
        """
        # Get the selected operation.
        sound_operation = self.operations._get(self._tool)
        if isinstance(sound_operation, SoundOperation):
            # Apply the operation to the editor
            suffix = sound_operation.handle(editor, suffix)
        elif isinstance(sound_operation, list):
            # Apply multiple operations to the editor
            for operation in sound_operation:
                suffix = operation.handle(editor, suffix)
        return suffix

    def start(self):
        """
        Process the sounds in the input folder synchronously.
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(self.start_async())
        except Exception as e:
            logger.error(e) 
    
    def __enter__(self):
        """
        Set up the context for sound processing.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clean up the context after sound processing.
        """
        pass