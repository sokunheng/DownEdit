
from abc import ABC, abstractmethod

from ._editor import AIImageEditor
from ....base import Operation


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