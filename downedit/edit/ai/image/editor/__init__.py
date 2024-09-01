from ._operation import AIImageOperation


class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> AIImageOperation:
        """
        Creates a ai image editing operation based on the operation name and parameters.
        """
        operations = {
            "rm_bg"      : lambda: None,
        }
        operation_class = operations.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)