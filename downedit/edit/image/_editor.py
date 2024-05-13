
class ImageEditor:
    
    def __init__(self):
        self.img_list = []
    
    def get_img_list(self, file_list):
        """ 
        Filter the provided list of files to return a list of image files 
        with extensions: 
        - jpg
        - jpeg
        - png
        """
        return [file for file in file_list if file.lower().endswith(('.jpg', '.jpeg', '.png'))]