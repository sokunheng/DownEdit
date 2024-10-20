
from abc import ABC, abstractmethod

from downedit.edit.base import Operation
from ._generator import AIImgGenerator


class AIImgGenOperation(Operation, ABC):
    """
    Abstract class for ai image operations.
    """
    @abstractmethod
    async def _run(self, gen: AIImgGenerator):
        pass

    async def handle(self, gen: AIImgGenerator, output_suffix: str) -> str:
        """
        Handles the operation and updates the output suffix.

        Args:
            gen (AIImgGenerator): The image generator instance.
            output_suffix (str): The current output suffix.

        Returns:
            str: The updated output suffix.
        """
        _img_url = await self._run(gen)
        return (
            _img_url,
            output_suffix + self.suffix
        )