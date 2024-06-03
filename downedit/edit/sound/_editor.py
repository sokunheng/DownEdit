import moviepy.editor as mp

from ...edit.base import Editor

class SoundEditor(Editor):
    def __init__(self, input_path = None, output_path = None):
        super().__init__(input_path, output_path)
        self.audio_clip = mp.AudioFileClip(self.input_path)
        
    def slow_and_reverb(self, slow_factor=0.8, reverb_time=0.5):
        """Slows down and adds reverb to an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            slow_factor (float, optional): Factor by which to slow down the audio (default: 0.8).
            reverb_time (float, optional): Reverb time in seconds (default: 0.5).
        """
        self.audio_clip = self.audio_clip.set_speed(
            slow_factor
        ).fx(
            mp.vfx.echo,
            delay=reverb_time,
            intensity=0.3
        )
        return self
    
    def render(
        self
    ):
        """
        Writes the modified audio to the specified output path.
        """
        try:
            self.audio_clip.write_audiofile(
                self.output_path,
                verbose=False,
                logger=None,
                codec='libvorbis',
                bitrate='3000k',
            )
        finally:
            self.audio_clip.close()