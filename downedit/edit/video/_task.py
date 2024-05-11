

from ..task import Task
from ._editor import VideoEditor
from ._operation import VideoOperation


class VideoTask(Task):
    """
    Task to be performed on video editor based on the selected operation.
    """
    def __init__(self, editor: VideoEditor):
        self.editor = editor
        
    def execute(self, operations: dict, threads, preset): ...
        