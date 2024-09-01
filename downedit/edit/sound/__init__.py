from ._operation import (
    SoundOperation,
    Volume,
    FadeIn,
    FadeOut
)

class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> SoundOperation:
        """
        Creates a video editing operation based on the operation name and parameters.

        Args:
            operation_name (str):
                - `Volume`: Change the volume of a sound.
                - `Fade In`: Fade in a sound.
                - `Fade Out`: Fade out a sound.

        Returns:
            SoundOperation: A sound operation object.
        """
        operations = {
            "Volume"     : Volume,
            "Fade In"    : FadeIn,
            "Fade Out"   : FadeOut
        }
        operation_class = operations.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)