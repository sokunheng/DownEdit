import time

from colorama import Fore

from ...utils.logger import Logger
from ...utils.file_utils import FileUtil

class ImageProcess:
    def __init__(
        self,
        tool: str,
        adjust_degrees: int,
        img_width: int,
        img_height: int,
        process_folder: str,
        output_folder: str
    ) -> None:
        self._tool = tool
        self._adjust_degrees = adjust_degrees
        self._img_width = img_width
        self._img_height = img_height
        self._input_folder = process_folder
        self._output_folder = output_folder
        self.logger = Logger("Programs")
    
    def process(self):
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
    
    def _process_image(self, clip) -> bool:
        """
        Process the video clip.
        
        Args:
            clip (str): The video clip path.
            
        Returns:
            bool: True if the video clip was processed successfully.
        """
        # Get the input filename without the extension
        file_name, file_extension = FileUtil.get_file_info(clip)
        limit_file_name = str(f'{file_name:60.60}')
        output_file_path = ""
        output_suffix = "" 
        return True