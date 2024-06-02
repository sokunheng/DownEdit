import os
import time

from colorama import Fore

from ..handler import Handler
from ...__config__ import Extensions
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
        **kwargs
    ) -> None:
        self._tool = tool
        self._adjust_degrees = kwargs.get("Degrees", 0)
        self._img_width = kwargs.get("Width", 540)
        self._img_height = kwargs.get("Height", 360)
        self._blur_radius = kwargs.get("Radius", 0.8)
        self._input_folder = FileUtil.get_file_list(
            directory=process_folder,
            extensions=Extensions.IMAGE
        )
        # Create the output folder.
        self._image_folder = FileUtil.create_folder(
            folder_type="EDITED_IMG"
        )
        # Get the output folder path based on the tool.
        self._output_folder = FileUtil.folder_path(
            folder_root=self._image_folder,
            directory_name=tool
        )
        self.logger = Logger("Programs")
        
        # Initialize the image operations
        self._flip_edit = Flip()
        self._crop_edit = Crop()
        self._enhance_edit = Enhance()
        self._rotate_edit = Rotate(self._adjust_degrees)
        self._resize_edit = Resize(self._img_width, self._img_height)
        self._grayscale_edit = GrayScale()
        self._sharpen_edit = Sharpen()
        self._blur_edit = Blur(self._blur_radius)
        
        # Initialize operations handler
        self.operations = Handler({
            " Flip Horizontal": self._flip_edit,
            " Crop Image": self._crop_edit,
            " Enhance Color": self._enhance_edit,
            " Rotate Image": self._rotate_edit,
            " Resize Image": self._resize_edit,
            " Grayscale Image": self._grayscale_edit,
            " Sharpen Image": self._sharpen_edit,
            " Blur Image": self._blur_edit
        })
    
    @staticmethod
    def get_tools() -> dict:
        """
        Get the available image editing tools.
        
        Returns:
            dict: The available image editing tools.
        """
        return { 
            " Flip Horizontal"   : {},
            " Crop Image"        : {},
            " Enhance Color"     : {},
            " Rotate Image"      : {"Degrees": int},
            " Resize Image"      : {"Width": int, "Height": int},
            " Grayscale Image"   : {},
            " Sharpen Image"     : {},
            " Blur Image"        : {"Radius": int},
        }
    
    def start(self):
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
        
        try:
            # Execute the operations and build the suffix
            image_editor = ImageEditor(image, output_file_path).load()
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
                
        except Exception as e:
            self.logger.file_error(e)
            return False

    
    def _build_and_apply_operations(self, editor: ImageEditor, suffix: str) -> str:
        """
        Build the suffix based on the operations and apply them to the editor.
        
        Args:
            editor (ImageEditor): The image editor.
            suffix (str): The current suffix.
            
        Returns:
            str: The updated suffix.
        """
        # Get the selected operation.
        image_operation = self.operations._get(self._tool)
        if isinstance(image_operation, ImageOperation):
            # Apply the operation to the editor
            suffix = image_operation.handle(editor, suffix)
        return suffix