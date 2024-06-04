CHUNK_SIZE = 1024
DE_VERSION = open('version', 'r').read().strip()

class Config:
    """
    A class that provides setting for different types of configurations.
    """
    def __init__(self) -> None:
        pass


class EditFolder:
    """
    A class that provides constants for different types of edits.
    """
    EDITED_VIDEO = "Edited_Video"
    EDITED_IMG = "Edited_Photo"
    EDITED_SOUND = "Edited_Sound"
    AI_Photo_Gen = "AI_Art"
    AI_Photo_Editor = "AI_Editor"

class Media:
    """
    A class that provides constants for different types of media.
    """
    YOUTUBE = "YouTube"
    TIKTOK = "Tiktok"
    DOUYIN = "Douyin"
    KUAISHOU = "Kuaishou"

class Extensions:
    """
    A class that provides constants for different types of extensions.
    """
    VIDEO = (".mp4", ".avi", ".mov", ".flv", ".wmv")
    IMAGE = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    SOUND = (".mp3", ".m4a", ".wav", ".ogg", ".wma", ".aac") 