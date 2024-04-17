
from abc import ABC, abstractmethod


class Editor(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def _apply_edit(self, **kwargs):
        pass
    
    def func(self, output_path, **kwargs):
        """
        Implement common editing logic
        """
        pass