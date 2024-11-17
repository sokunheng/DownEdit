from downedit.edit.ai.cloud.image import AIImgGenProcess
from downedit.edit import (
    VideoProcess,
    SoundProcess,
    ImageProcess
)


TOOLS = {
    "edit_video"        : VideoProcess,
    "edit_image"        : ImageProcess,
    "edit_sound"        : SoundProcess,
    "generate_ai_image" : AIImgGenProcess,
}


def get_tool(tool_name: str):
    """
    Retrieves the tool class from the registry.

    Args:
        tool_name (str): The name of the tool to retrieve.
    """
    return TOOLS.get(tool_name)