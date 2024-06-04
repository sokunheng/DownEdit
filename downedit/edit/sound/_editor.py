import moviepy.editor as mp

from ...edit.base import Editor

class SoundEditor(Editor):
    def __init__(self, input_path = None, output_path = None):
        super().__init__(input_path, output_path)
        self.audio_clip = mp.AudioFileClip(self.input_path)
        
    def speed(self, slow_factor=0.8):
        """Manipulate speed to an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            slow_factor (float, optional): Factor by which to slow down the audio (default: 0.8).
            reverb_time (float, optional): Reverb time in seconds (default: 0.5).
        """
        self.audio_clip = self.audio_clip.set_speed(slow_factor)
        return self
    
    def reverb(self, reverb_time=0.5):
        """Adds reverb to an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            reverb_time (float, optional): Reverb time in seconds (default: 0.5).
        """ 
        self.audio_clip = self.audio_clip.fx(
            mp.vfx.echo,
            delay=reverb_time,
            intensity=0.3
        )
        return self
    
    def bass_boost(self, factor=2, frequencies=30):
        """
        Applies a bass boost effect to an audio clip.

        Args:
            clip: The audio clip to modify.
            factor: The amount of bass boost to apply (higher value = more bass boost).

        Returns:
            The modified audio clip with bass boost applied.
        """
        self.audio_clip = self.audio_clip.eq(boost_db=factor, bands=[frequencies])
        return self
    
    def volume(self, volume=0.5):
        """Changes the volume of an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            volume (float, optional): Volume level (default: 0.5).
        """
        self.audio_clip = self.audio_clip.volumex(volume)
        return self
    
    def fade_in(self, duration=2):
        """Fades in an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            duration (float, optional): Fade-in duration in seconds (default: 2).
        """
        self.audio_clip = self.audio_clip.audio_fadein(duration)
        return self
    
    def fade_out(self, duration=2):
        """Fades out an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            duration (float, optional): Fade-out duration in seconds (default: 2).
        """
        self.audio_clip = self.audio_clip.audio_fadeout(duration)
        return self
    
    def loop(self, n=2):
        """Loops an audio file.

        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            n (int, optional): Number of times to loop the audio (default: 2).
        """
        self.audio_clip = self.audio_clip.fx(
            mp.audio.fx.all,
            n=n
        )
        return self

    def phaser(
        self,
        gain_in=0.5,
        gain_out=0.5,
        delay=1,
        decay=0.5,
        speed=0.5,
        triangular=False
    ):
        """Adds a phaser effect to an audio file.
        
        Args:
            audio_path (str): Path to the input audio file.
            output_path (str): Path to save the processed audio file.
            gain_in (float, optional): Input gain (default: 0.5).
            gain_out (float, optional): Output gain (default: 0.5).
            delay (float, optional): Delay in seconds (default: 1).
            decay (float, optional): Decay (default: 0.5).
            speed (float, optional): Speed (default: 0.5).
            triangular (bool, optional): Use triangular waveform (default: False).
        """
        
        self.audio_clip = self.audio_clip.fx(
            mp.audio.fx.phaser,
            gain_in=gain_in,
            gain_out=gain_out,
            delay=delay,
            decay=decay,
            speed=speed,
            triangular=triangular
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