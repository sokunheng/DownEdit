from ...edit.base import Editor

class SoundEditor(Editor):
    def __init__(self, input_path = None, output_path = None):
        super().__init__(input_path, output_path)
        