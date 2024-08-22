from ._operation import (
    ImageOperation,
    Flip,
    Crop,
    Enhance,
    Rotate,
    Resize,
    GrayScale,
    Sharpen,
    Blur
)

class OperationFactory:
    @staticmethod
    def create(operation_name: str, **kwargs) -> ImageOperation:
        """
        Creates a video editing operation based on the operation name and parameters.
        """
        operations = {
            "flip"      : Flip,
            "crop"      : Crop,
            "enhance"   : Enhance,
            "rotate"    : Rotate,
            "resize"    : Resize,
            "grayscale" : GrayScale,
            "sharpen"   : Sharpen,
            "blur"      : Blur
        }
        operation_class = operations.get(operation_name.lower())
        if operation_class is None:
            raise ValueError(f"Invalid operation name: {operation_name}")
        return operation_class(**kwargs)