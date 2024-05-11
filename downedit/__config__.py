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
