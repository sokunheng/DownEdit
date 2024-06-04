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

class Speed(SoundOperation):
    """
    Slows down the audio clip by a factor.
    """
    def __init__(self, factor=0.8):
        super().__init__(
            name="Speed",
            function=self._run,
            suffix=f"_speed_{factor}x"
        )
        self.factor = factor

    def _run(self, editor: SoundEditor):
        editor.speed(self.factor)
        
class Reverb(SoundOperation):
    """
    Adds reverb to the audio clip.
    """
    def __init__(self, reverb_time=0.5):
        super().__init__(
            name="Reverb",
            function=self._run,
            suffix="_reverb"
        )
        self.reverb_time = reverb_time

    def _run(self, editor: SoundEditor):
        editor.reverb(self.reverb_time)

class BassBoost(SoundOperation):
    """
    Applies a bass boost effect to the audio clip.
    """
    def __init__(self, factor=2, frequencies=30):
        super().__init__(
            name="Bass Boost",
            function=self._run,
            suffix="_bassboost"
        )
        self.factor = factor
        self.frequencies = frequencies

    def _run(self, editor: SoundEditor):
        editor.bass_boost(self.factor, self.frequencies)

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

class Loop(SoundOperation):
    """
    Loops the audio clip for a specified number of times.
    """
    def __init__(self, amount=2):
        super().__init__(
            name="Loop",
            function=self._run,
            suffix=f"_looped_{amount}x"
        )
        self.amount = amount

    def _run(self, editor: SoundEditor):
        editor.loop(self.amount)

class Pharser(SoundOperation):
    """
    Adds a phaser effect to the audio clip.
    """
    def __init__(
        self,
        gain_in=0.5,
        gain_out=0.5,
        delay=1,
        decay=0.5,
        speed=0.5,
        triangular=False
    ):
        super().__init__(
            name="Phaser",
            function=self._run,
            suffix="_phaser"
        )
        self.gain_in = gain_in
        self.gain_out = gain_out
        self.delay = delay
        self.decay = decay
        self.speed = speed
        self.triangular = triangular

    def _run(self, editor: SoundEditor):
        editor.phaser(
            gain_in=self.gain_in,
            gain_out=self.gain_out,
            delay=self.delay,
            decay=self.decay,
            speed=self.speed,
            triangular=self.triangular
        )

