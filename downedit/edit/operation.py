from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self, name: str, function: callable, suffix: str):
        """
        Initializes an ImageAction object.

        Args:
            name (str): The human-readable name of the action.
            function (callable): The function reference that performs the action.
            suffix (str): The suffix to be appended to processed filenames.
        """
        self.name = name
        self.function = function
        self.suffix = suffix