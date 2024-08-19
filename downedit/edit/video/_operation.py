
from abc import ABC, abstractmethod

from ..base import Operation
from ._editor import VideoEditor


class VideoOperation(Operation, ABC):
    """
    Abstract class for video operations.
    """
    @abstractmethod
    def _run(self, editor: VideoEditor):
        pass

    def handle(self, editor: VideoEditor, output_suffix: str) -> str:
        """
        Handles the operation and updates the output suffix.

        Args:
            editor (VideoEditor): The video editor instance.
            output_suffix (str): The current output suffix.

        Returns:
            str: The updated output suffix.
        """
        self._run(editor)
        return output_suffix + self.suffix

class Flip(VideoOperation):
    """
    Flips the video clip horizontally.
    """
    def __init__(self):
        super().__init__(
            name="Flip Horizontal",
            function=self._run,
            suffix="_flipped"
        )

    def _run(self, editor: VideoEditor):
        editor.flip()

class Speed(VideoOperation):
    """
    Speeds up the video clip by a factor.
    """
    def __init__(self, factor=1.0):
        super().__init__(
            name=f"Speed Up",
            function=self._run,
            suffix=f"_spedup_{int(factor)}x"
        )
        self.factor = factor

    def _run(self, editor: VideoEditor):
        editor.speed(self.factor)

class AddMusic(VideoOperation):
    """
    Adds music to the video clip.
    """
    def __init__(self, music_path):
        super().__init__(
            name="Add Music",
            function=self._run,
            suffix="_with_music"
        )
        self.music_path = music_path

    def _run(self, editor: VideoEditor):
        editor.add_music(self.music_path)

class Loop(VideoOperation):
    """
    Loops the video for a specified number of times.
    """
    def __init__(self, amount=1):
        super().__init__(
            name=f"Loop",
            function=self._run,
            suffix=f"_looped_{amount}x"
        )
        self.amount = amount

    def _run(self, editor: VideoEditor):
        editor.loop(self.amount)

class AdjustColor(VideoOperation):
    """
    Adjusts the color properties (brightness, contrast, saturation) of the video.
    """
    def __init__(self, brightness=1, contrast=1, saturation=1):
        super().__init__(
            name="Adjust Color",
            function=self._run,
            suffix="_color_adjusted"
        )
        self.brightness = brightness
        self.contrast = contrast
        self.saturation = saturation

    def _run(self, editor: VideoEditor):
        editor.adjust_color(
            self.brightness,
            self.contrast,
            self.saturation
        )