from typing import Dict, List

from . import OperationFactory

from ... import Extensions
from ...utils.file_utils import FileUtil

from downedit.edit.image._editor import ImageEditor
from downedit.edit.image._task import ImageTask

from ..base import Handler
from ..process import Process


class ImageProcess(Process):
    """
    Processes images based on the selected tool.
    """

    def __init__(
        self,
        tool: str,
        process_folder: str,
        batch_size: int = 5,
        **kwargs
    ):
        self._tool = tool
        self._adjust_degrees = kwargs.get("Degrees", 0)
        self._img_width = kwargs.get("Width", 540)
        self._img_height = kwargs.get("Height", 360)
        self._blur_radius = kwargs.get("Radius", 0.8)
        super().__init__(tool, process_folder, batch_size, **kwargs)

    def _get_input_files(self, process_folder: str) -> List[str]:
        """
        Gets the list of input images.
        """
        return FileUtil.get_file_list(
            directory=process_folder,
            extensions=Extensions.IMAGE
        )

    def _get_output_folder(self, tool: str) -> str:
        """
        Gets the output folder path for edited images.
        """
        return FileUtil.folder_path(
            folder_root=FileUtil.create_folder(folder_type="EDITED_IMG"),
            directory_name=tool
        )

    def _init_operations(self, **kwargs) -> Handler:
        """
        Initializes the image operations based on the selected tool.
        """
        _flip_edit         = OperationFactory.create("flip")
        _crop_edit         = OperationFactory.create("crop")
        _enhance_edit      = OperationFactory.create("enhance")
        _rotate_edit       = OperationFactory.create("rotate", degrees=self._adjust_degrees)
        _resize_edit       = OperationFactory.create("resize", width=self._img_width, height=self._img_height)
        _grayscale_edit    = OperationFactory.create("grayscale")
        _sharpen_edit      = OperationFactory.create("sharpen")
        _blur_edit         = OperationFactory.create("blur", radius=self._blur_radius)

        return Handler({
            " Flip Horizontal"  : _flip_edit,
            " Crop Image"       : _crop_edit,
            " Enhance Color"    : _enhance_edit,
            " Rotate Image"     : _rotate_edit,
            " Resize Image"     : _resize_edit,
            " Grayscale Image"  : _grayscale_edit,
            " Sharpen Image"    : _sharpen_edit,
            " Blur Image"       : _blur_edit
        })

    def _get_task(self) -> ImageTask:
        """
        Gets the image task.
        """
        return ImageTask()

    def _create_editor(self, media_path: str) -> ImageEditor:
        """
        Creates an ImageEditor object.
        """
        return ImageEditor(media_path)

    @staticmethod
    def get_tools() -> Dict[str, Dict[str, type]]:
        """
        Get the available image editing tools.
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