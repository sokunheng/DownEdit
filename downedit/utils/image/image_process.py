import os
import time

from colorama import *
from pystyle import *
from rich.traceback import install
from rich.console import Console
from datetime import datetime
from PIL import Image

from downedit.utils.common import *
from downedit.utils.image.ml.ai_remove_bg import remove_background

class RenderImage:
    def __init__(self) -> None:
        pass
    
    def _remove_bg(
        model_dir,
        input_imag_path,
        img_name,
        img_extension,
        output_imag_path
    ):
        
        output_path = os.path.join(
            output_imag_path,
            f"{img_name}{img_extension}"
        )
        limit = str(f'{img_name:60.60}')

        
        if os.path.exists(output_path):
            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[File] {Fore.WHITE}{limit} already exists, skipping...")
            return
        
        print(f"{Fore.CYAN}[{datetime.now().strftime("%H:%M:%S")}] {Fore.GREEN}[File] {Fore.WHITE}{limit}")
        
        start = time.time()
        output_img = remove_background(
            model_dir=model_dir,
            input_imag_path=input_imag_path,
            output_imag_path=output_path
        )
        end = time.time()

        print(
            f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Timelapsed:{Fore.YELLOW} "+ f"%.2fs" % (end - start)
        )
        print(
            f"{Fore.YELLOW}[{datetime.now().strftime("%H:%M:%S")}] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n"
        )
        
        return output_img
    
    def _get_properties(self, source_image):
        img = Image.open(source_image)
        width, height = img.size
        
        min_side_length = min(width, height)

        left = (width - min_side_length) / 2
        upper = (height - min_side_length) / 2
        right = (width + min_side_length) / 2
        lower = (height + min_side_length) / 2
        
        return left, upper, right, lower
        
    def _get_image_boundaries(self, source_image):
        maskColor = (255, 255, 255, 255)
        invalidImage = False
        iX = 0
        iY = 0
        leftHandImageBoundary = 0
        rightHandImageBoundary = 0
        topImageBoundary = 0
        bottomImageBoundary = 0
        img = Image.open(source_image)
        arr = img.load()
        imageWidth, imageHeight = img.size
        
        while maskColor == arr[iX, iY] and invalidImage == False: 
            if iX == imageWidth - 2 and iY == imageHeight - 2: 
                invalidImage = True
            if iX < imageWidth:
                iX = iX + 1
            if iX >= imageWidth:
                iX = 0
                iY = iY + 1
            
        topImageBoundary = iY

        iY = imageHeight - 1
        iX = 0
        
        while maskColor == arr[iX, iY]and invalidImage == False:
            if iX < imageWidth:
                iX = iX + 1
            if iX >= imageWidth:
                iX = 0
                iY = iY - 1
        
        bottomImageBoundary = iY
        
        iY = 0
        iX = 0
        
        while maskColor == arr[iX, iY] and invalidImage == False:
            if iY < imageHeight:
                iY = iY + 1
            if iY >= imageHeight:
                iY = 0
                iX = iX + 1
        
        leftHandImageBoundary = iX
        
        iY = 0
        iX = imageWidth - 1
        
        while maskColor == arr[iX, iY] and invalidImage == False:
            if iY < imageHeight:
                iY = iY + 1
            if iY >= imageHeight:
                iY = 0
                iX = iX - 1
        
        rightHandImageBoundary = iX

        if invalidImage == True:
            print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[File] {Fore.WHITE}No content was found in this image that can be edited, skipping...")   
            return 0, 0, 0, 0, True

        return leftHandImageBoundary, rightHandImageBoundary, topImageBoundary, bottomImageBoundary, invalidImage


    def _crop_img(
        self,
        input_imag_path,
        img_name,
        img_extension, 
        output_folder
    ):
        
        output_img_path = os.path.join(output_folder, f"{img_name}{img_extension}")
        
        # left, right, top, bottom, invalid_image = self._get_image_boundaries(input_imag_path)
        
        left, top, right, bottom = self._get_properties(input_imag_path)
        
        # if invalid_image:
        #     print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[File] {Fore.WHITE}No content was found in this image that can be edited, skipping...")
        #     return

        img = Image.open(input_imag_path)
        img_res = img.crop((left, top, right, bottom))
        
        img_res.save(output_img_path)
        img_res.close()
        img.close()
    
    def _flip_img(self, input_imag_path, img_name, img_extension, output_folder):
        
        output_img_path = os.path.join(output_folder, f"{img_name}{img_extension}")
        
        img = Image.open(input_imag_path)
        img_res = img.transpose(Image.FLIP_LEFT_RIGHT)

        img_res.save(output_img_path)
        img_res.close()
        img.close()