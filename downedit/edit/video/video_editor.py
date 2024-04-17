from moviepy.editor import *

class VideoEditor:
    
    def __init__(self):
        self.clip_list = []

    def get_clip_list(self, file_list):
        """ 
        Filter the provided list of files to return a list of video files 
        with extensions: 
        - mp4
        - mkv
        - avi
        - webm
        - mov
        """
        return [file for file in file_list if file.lower().endswith(('.mp4', '.mkv', '.avi', '.webm', '.mov'))]

    def flip(self, input_path, output_path, threads: int, preset):
        """
        Flips the video horizontally and writes the modified video to the output path.
        """
        clip = VideoFileClip(input_path)
        clip = clip.fx(vfx.mirror_x)
        clip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        clip.close()

    def change_speed(self, input_path, speed_factor, output_path, threads: int, preset):
        """
        Changes the speed of the video based on the provided speed factor and writes the modified video to the output path.
        """
        clip = VideoFileClip(input_path)
        clip = clip.fx(vfx.speedx, speed_factor)
        clip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        clip.close()

    def flip_and_change_speed(self, input_path, speed_factor, output_path, threads: int, preset):
        """
        Flips the video horizontally and changes its speed, then writes the modified video to the output path.
        """
        clip = VideoFileClip(input_path)
        clip = clip.fx(vfx.mirror_x).fx(vfx.speedx, speed_factor)
        clip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        clip.close()

    def add_background_music(self, input_path, music_path, output_path, threads: int, preset):
        """
        Adds background music to the video and writes the modified video to the output path.
        """
        videoclip = VideoFileClip(input_path)
        clip_duration = videoclip.duration
        audioclip = AudioFileClip(music_path)
        new_audioclip = afx.audio_loop(audioclip, duration=clip_duration)
        videoclip = videoclip.set_audio(new_audioclip)
        videoclip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        videoclip.close()

    def change_speed_and_add_music(self, input_path, music_path, speed_factor, output_path, threads: int, preset):
        """
        Changes the speed of the video, adds background music, and writes the modified video to the output path.
        """
        videoclip = VideoFileClip(input_path)
        clip_duration = videoclip.duration
        final_duration = clip_duration / speed_factor
        audioclip = AudioFileClip(music_path)
        new_audioclip = afx.audio_loop(audioclip, duration=final_duration)
        videoclip = videoclip.fx(vfx.speedx, speed_factor).set_audio(new_audioclip)
        videoclip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        videoclip.close()

    def change_speed_add_music_and_flip(self, input_path, music_path, speed_factor, output_path, threads: int, preset):
        """
        Flips the video horizontally, changes its speed, adds background music, and writes the modified video to the output path.
        """
        videoclip = VideoFileClip(input_path)
        clip_duration = videoclip.duration
        final_duration = clip_duration / speed_factor
        audioclip = AudioFileClip(music_path)
        new_audioclip = afx.audio_loop(audioclip, duration=final_duration)
        videoclip = videoclip.fx(vfx.mirror_x).fx(vfx.speedx, speed_factor).set_audio(new_audioclip)
        videoclip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        videoclip.close()

    def color_correction(self, input_path, output_path, threads: int, preset, brightness=1, contrast=1, saturation=1):
        """
        Adjusts the color properties (brightness, contrast, saturation) of the video and writes the modified video to the output path.
        """
        clip = VideoFileClip(input_path)
        clip = clip.fx(vfx.colorx, factor=brightness).fx(vfx.colorx, contrast=contrast).fx(vfx.colorx, saturation=saturation)
        clip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", threads=threads ,preset=preset)
        clip.close()
