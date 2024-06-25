import asyncio
import os
import time

from ...utils.console import Console
from ..base import Handler
from ...__config__ import Extensions
from ...utils.logger import logger
from ...utils.observer import Observer
from ...utils.file_utils import FileUtil
from ._editor import ImageEditor
from ._task import ImageTask
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
        self.image_task = ImageTask()
        self.observer = Observer()
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
        
        # Initialize the image operations
        self._flip_edit         = Flip()
        self._crop_edit         = Crop()
        self._enhance_edit      = Enhance()
        self._rotate_edit       = Rotate(self._adjust_degrees)
        self._resize_edit       = Resize(self._img_width, self._img_height)
        self._grayscale_edit    = GrayScale()
        self._sharpen_edit      = Sharpen()
        self._blur_edit         = Blur(self._blur_radius)
        
        # Initialize operations handler
        self.operations = Handler({
            " Flip Horizontal"  : self._flip_edit,
            " Crop Image"       : self._crop_edit,
            " Enhance Color"    : self._enhance_edit,
            " Rotate Image"     : self._rotate_edit,
            " Resize Image"     : self._resize_edit,
            " Grayscale Image"  : self._grayscale_edit,
            " Sharpen Image"    : self._sharpen_edit,
            " Blur Image"       : self._blur_edit
        })
    
    @staticmethod
    def get_tools() -> dict:
        """
        Get the available image editing tools.
        
        Returns:
            dict: The available image editing tools.
        """
        return { 
            " Flip Horizontal"  : {},
            " Crop Image"       : {},
            " Enhance Color"    : {},
            " Rotate Image"     : {"Degrees": int},
            " Resize Image"     : {"Width": int, "Height": int},
            " Grayscale Image"  : {},
            " Sharpen Image"    : {},
            " Blur Image"       : {"Radius": int},
        }
    
    async def start_async(self):
        """
        Process the images in the input folder asynchronously.
        """
        proceed_count = 0
        start = time.time()
        for image in self._input_folder:
            if self.observer.is_termination_signaled():
                break
            if await self._process_image(image):
                proceed_count += 1
            else:
                continue
            
        await self.image_task.execute()
        await self.image_task.close()  
        end = time.time()
        
        logger.info(f"Processed: "+ f"%.2fs" % (end - start))
        logger.file(f"Saved at [green]{self._output_folder}[/green]")
        logger.file(f"Processed [green]{proceed_count}[/green] images successfully.")
        logger.pause()

    async def _process_image(self, image) -> bool:
        """
        Process the video clip.
        
        Args:
            clip (str): The video clip path.
            
        Returns:
            bool: True if the video clip was processed successfully.
        """
        try:
            
            # Execute the operations and build the suffix
            image_editor = ImageEditor(image).load()
            output_suffix = self._build_and_apply_operations(image_editor, "")
            
            # Construct the output file path with filename, suffix, and extension
            file_info = FileUtil.get_file_info(image)
            file_name, file_extension, file_size = file_info
            full_file = f"{file_name}{output_suffix}"
            output_file_path = FileUtil.get_output_file(
                self._output_folder,
                full_file,
                file_extension
            ) 

            # Set the final output path
            image_editor.output_path = output_file_path

            # Save the image
            await self.image_task.add_task(
                operation_function=image_editor.render,
                operation_image=(
                    output_file_path,
                    f"{file_name}{file_extension}",
                    file_size
                )
            )
            return True
                
        except Exception as e:
            logger.error(e)
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
    
    def start(self):
        """
        Process the images in the input folder synchronously.
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(self.start_async())
        except Exception as e:
            logger.error(e) 
    
    def __enter__(self):
        """
        Set up the context for image processing.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clean up the context after image processing.
        """
        pass