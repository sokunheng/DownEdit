from abc import ABC, abstractmethod

from ..base import Operation
from ._editor import SoundEditor


class SoundOperation(Operation, ABC):
    """
    Abstract class for sound operations.
    """
    @abstractmethod
    def _run(self, editor: SoundEditor):
        pass
    
    def handle(self, editor: SoundEditor, output_suffix: str) -> str:
        """
        Handles the operation and updates the output suffix.

        Args:
            editor (SoundEditor): The sound editor instance.
            output_suffix (str): The current output suffix.

        Returns:
            str: The updated output suffix.
        """
        self._run(editor)
        return output_suffix + self.suffix

class Volume(SoundOperation):
    """
    Changes the volume of the audio clip.
    """
    def __init__(self, volume=0.5):
        super().__init__(
            name="Volume",
            function=self._run,
            suffix="_volume"
        )
        self.volume = volume

    def _run(self, editor: SoundEditor):
        editor.volume(self.volume)

class FadeIn(SoundOperation):
    """
    Fades in the audio clip.
    """
    def __init__(self, duration=2):
        super().__init__(
            name="Fade In",
            function=self._run,
            suffix="_fadein"
        )
        self.duration = duration

    def _run(self, editor: SoundEditor):
        editor.fade_in(self.duration)

class FadeOut(SoundOperation):
    """
    Fades out the audio clip.
    """
    def __init__(self, duration=2):
        super().__init__(
            name="Fade Out",
            function=self._run,
            suffix="_fadeout"
        )
        self.duration = duration

    def _run(self, editor: SoundEditor):
        editor.fade_out(self.duration)