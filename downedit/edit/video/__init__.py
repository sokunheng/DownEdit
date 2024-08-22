from ._operation import (
    VideoOperation,
    Flip,
    Speed,
    AddMusic,
    Loop,
    AdjustColor
)

class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> VideoOperation:
        """
        Creates a video editing operation based on the operation name and parameters.
        """
        operations = {
            "flip"        : Flip,
            "speed"       : Speed,
            "add_music"   : AddMusic,
            "loop"        : Loop,
            "adjust_color": AdjustColor,
        }
        operation_class = operations.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)