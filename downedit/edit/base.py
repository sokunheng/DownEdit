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


class Handler:
    """
    This class holds a dictionary of manipulation actions.
    """

    def __init__(self, actions_dict: dict):
        """
        Initializes the handler with a dictionary of actions.

        Args:
            actions_dict (dict): A dictionary where keys are operation names
                (strings) and values are dictionaries containing details like
                'name' (string), 'function' (callable), and 'suffix' (string).
        """
        self.actions = actions_dict

    def _get(self, operation: str) -> dict:
        """
        Retrieves the action details (name, function, suffix) based on the operation name.

        Args:
            operation (str): The name of the desired manipulation operation.

        Returns:
            dict: A dictionary containing the retrieved action details, or None if not found.
                The structure is {'name': str, 'function': callable, 'suffix': str}.
        """
        return self.actions.get(operation)


class Operation(ABC):
    def __init__(self, name: str, function: callable, suffix: str):
        """
        Initializes an Operation object.

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


class Task(ABC):
    """
    Abstract class for tasks to be performed.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def execute(self):
        pass

    @abstractmethod
    async def close(self) -> None:
        pass