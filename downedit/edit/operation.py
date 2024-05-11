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
        self._name = name
        self._function = function
        self._suffix = suffix
    
    @property
    def name(self):
        return self._name 
    
    @property
    def function(self):
        return self._function
    
    @property
    def suffix(self):
        return self._suffix