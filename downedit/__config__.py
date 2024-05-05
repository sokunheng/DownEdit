CHUNK_SIZE = 1024
DE_VERSION = open('version', 'r').read().strip()
            
class EditFolder:
    """
    A class that provides constants for different types of edits.
    """
    def __init__(self):
        self.EDITED_VIDEO = "Edited_Video"
        self.EDITED_IMG = "Edited_Photo"
        self.AI_Photo_Gen = "AI_Art"
        self.AI_Photo_Editor = "AI_Editor"
        

class Media:
    """
    A class that provides constants for different types of media.
    """
    def __init__(self):
        self.YOUTUBE = "YouTube"
        self.TIKTOK = "Tiktok"
        self.DOUYIN = "Douyin"
        self.KUAISHOU = "Kuaishou"
