
from abc import ABC, abstractmethod

from downedit.edit.base import Operation
from ._editor import AIImageEditor


class AIImageOperation(Operation, ABC):
    """
    Abstract class for image operations.
    """
    @abstractmethod
    def _run(self, editor: AIImageEditor):
        pass

    def handle(self, editor: AIImageEditor, output_suffix: str) -> str:
        """
        Handles the operation and updates the output suffix.

        Args:
            editor (ImageEditor): The image editor instance.
            output_suffix (str): The current output suffix.

        Returns:
            str: The updated output suffix.
        """
        self._run(editor)
        return output_suffix + self.suffix

class RemoveBG(AIImageOperation):
    """
    Flips the image horizontally.
    """
    def __init__(self):
        super().__init__(
            name="Remove Background",
            function=self._run,
            suffix="_removed_bg"
        )

    def _run(self, editor: AIImageEditor):
        editor.remove_bg()