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