
from abc import ABC, abstractmethod


class Editor(ABC):
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        
    def func(self, **kwargs):
        """
        Implement common editing logic
        """
        pass

    @abstractmethod
    def render(self, **kwargs):
        pass