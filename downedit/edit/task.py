from abc import ABC, abstractmethod


class Task(ABC):
    """
    Abstract class for tasks to be performed on editor.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass