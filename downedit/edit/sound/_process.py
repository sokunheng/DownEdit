import os
import time

from colorama import Fore

from ..base import Handler
from ...__config__ import Extensions
from ...utils.logger import logger
from ...utils.file_utils import FileUtil
from ._editor import SoundEditor
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
        **kwargs
    ) -> None:
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
    
    def start(self):
        """
        Process the sound clips in the input folder.
        """
        proceed_count = 0
        start = time.time()
        for sound in self._input_folder:
            if self._process_sound(sound):
                proceed_count += 1
            else:
                continue
        end = time.time()
        
        logger.info(f"Processed: "+ f"%.2fs" % (end - start))
        logger.file(f"Saved at [green]{self._output_folder}[/green]")
        logger.file(f"Processed [green]{proceed_count}[/green] sound successfully.")
        logger.pause()
    
    def _process_sound(self, sound) -> bool:
        """
        Process the sound clip.
        
        Args:
            clip (str): The sound clip path.
            
        Returns:
            bool: True if the sound clip was processed successfully.
        """
        # Get the input filename without the extension
        file_name, file_extension, file_size = FileUtil.get_file_info(sound)
        limit_file_name = str(f'{file_name:60.60}')
        output_file_path = ""
        output_suffix = "" 
        
        try:
            # Execute the operations and build the suffix
            sound_editor = SoundEditor(sound, output_file_path)
            output_suffix = self._build_and_apply_operations(sound_editor, output_suffix)
            
            # Construct the output file path with filename, suffix, and extension
            output_file_path = FileUtil.get_output_file(
                self._output_folder,
                f"{file_name}{output_suffix}",
                file_extension
            )
            
            if os.path.exists(output_file_path):
                logger.error(
                    f"Output file already exists - {limit_file_name}{output_suffix}{file_extension}"
                )
                return False
            
            logger.info(
                f"Processing: [green]{limit_file_name}[/green]"
            )
            # Set the final output path
            sound_editor.output_path = output_file_path
            # Save the sound
            sound_editor.render()
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