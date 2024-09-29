from ._operation import (
    AIImageOperation,
    RemoveBG
)


class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> AIImageOperation:
        """
        Creates a ai image editing operation based on the operation name and parameters.

        Args:
            operation_name (str):
                - `rm_bg`: Remove background from an image.

        Returns:
            AIImageOperation: An ai image operation object.
        """
        operations = {
            "rm_bg"      : RemoveBG,
        }
        operation_class = operations.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)