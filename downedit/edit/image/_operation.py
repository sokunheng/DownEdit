from abc import ABC, abstractmethod

from ..base import Operation
from ._editor import ImageEditor

class ImageOperation(Operation, ABC):
    """
    Abstract class for image operations.
    """
    @abstractmethod
    def _run(self, editor: ImageEditor):
        pass
    
    def handle(self, editor: ImageEditor, output_suffix: str) -> str:
        """
        Handles the operation and updates the output suffix.

        Args:
            editor (ImageEditor): The image editor instance.
            output_suffix (str): The current output suffix.

        Returns:
            str: The updated output suffix.
        """
        self._run(editor)
        return output_suffix + self.suffix

class Flip(ImageOperation):
    """
    Flips the image horizontally.
    """
    def __init__(self):
        super().__init__(
            name="Flip Horizontal",
            function=self._run,
            suffix="_flipped"
        )
    
    def _run(self, editor: ImageEditor):
        editor.transpose()

class Crop(ImageOperation):
    """
    Crops the image.
    """
    def __init__(self):
        super().__init__(
            name="Crop Image",
            function=self._run,
            suffix="_cropped"
        )
    
    def _run(self, editor: ImageEditor):
        editor.crop()

class Enhance(ImageOperation):
    """
    Enhance the color of the image.
    """
    def __init__(self):
        super().__init__(
            name="Adjust Color",
            function=self._run,
            suffix="_enhanced"
        )

    def _run(self, editor: ImageEditor):
        editor.enhance()
        
class Rotate(ImageOperation):
    """
    Rotates the image.
    """
    def __init__(self, degrees=0):
        super().__init__(
            name=f"Rotate Image",
            function=self._run,
            suffix=f"_rotated_{degrees}deg"
        )
        self.degrees = degrees

    def _run(self, editor: ImageEditor):
        editor.rotate(self.degrees)

class Resize(ImageOperation):
    """
    Resizes the image.
    """
    def __init__(self, width=540, height=360):
        super().__init__(
            name="Resize Image",
            function=self._run,
            suffix="_resized"
        )
        self.width = width
        self.height = height

    def _run(self, editor: ImageEditor):
        editor.resize(self.width, self.height)

class GrayScale(ImageOperation):
    """
    Converts the image to grayscale.
    """
    def __init__(self):
        super().__init__(
            name="GrayScale Image",
            function=self._run,
            suffix="_gray"
        )
    
    def _run(self, editor: ImageEditor):
        editor.grayscale()

class Sharpen(ImageOperation):
    """
    Sharpens the image.
    """
    def __init__(self):
        super().__init__(
            name="Sharpen Image",
            function=self._run,
            suffix="_sharpened"
        )

    def _run(self, editor: ImageEditor):
        editor.sharpen()

class Blur(ImageOperation):
    """
    Blurs the image.
    """
    def __init__(self, radius = 2):
        super().__init__(
            name="Blur Image",
            function=self._run,
            suffix="_blurred"
        )
        self.radius = radius

    def _run(self, editor: ImageEditor):
        editor.blur(self.radius)