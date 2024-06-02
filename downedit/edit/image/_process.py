import os
import time

from colorama import Fore

from ...utils.logger import Logger
from ...utils.file_utils import FileUtil
from ._editor import ImageEditor
from ._operation import (
    ImageOperation,
    Flip,
    Crop,
    Enhance,
    Rotate,
    Resize,
    GrayScale,
    Sharpen,
    Blur
)


class ImageProcess:
    def __init__(
        self,
        tool: str,
        process_folder: str,
        output_folder: str,
        **kwargs
    ) -> None:
        self._tool = tool
        self._adjust_degrees = kwargs.get("Degrees", 0)
        self._img_width = kwargs.get("Width", 0)
        self._img_height = kwargs.get("Height", 0)
        self._blur_radius = kwargs.get("Radius", 1)
        self._input_folder = process_folder
        self._output_folder = output_folder
        self.logger = Logger("Programs")
    
    def process(self):
        """
        Process the video clips in the input folder.
        """
        proceed_count = 0
        start = time.time()
        for image in self._input_folder:
            if self._process_image(image):
                proceed_count += 1
            else:
                continue
        end = time.time()
        
        self.logger.info(f"Processed:{Fore.YELLOW} "+ f"%.2fs" % (end - start))
        self.logger.file_info(f"Saved at [green]{self._output_folder}[/green]")
        self.logger.file_info(f"Processed [green]{proceed_count}[/green] images successfully.")
        self.logger.keybind("Press enter to continue..")
    
    def _process_image(self, image) -> bool:
        """
        Process the video clip.
        
        Args:
            clip (str): The video clip path.
            
        Returns:
            bool: True if the video clip was processed successfully.
        """
        # Get the input filename without the extension
        file_name, file_extension, file_size = FileUtil.get_file_info(image)
        limit_file_name = str(f'{file_name:60.60}')
        output_file_path = ""
        output_suffix = "" 
        
        # Execute the operations and build the suffix
        image_editor = ImageEditor(image, output_file_path)
        output_suffix = self._build_and_apply_operations(image_editor, output_suffix)
        
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
        image_editor.output_path = output_file_path
        # Save the image
        image_editor.render()
        return True
    
    def _build_and_apply_operations(self, editor: ImageEditor, suffix: str) -> str:
        """
        Build the suffix based on the operations and apply them to the editor.
        
        Args:
            editor (ImageEditor): The image editor.
            suffix (str): The current suffix.
            
        Returns:
            str: The updated suffix.
        """
        operations = self._get_operations()
        for operation in operations:
            suffix += operation.suffix
            operation.function(editor)
        return suffix