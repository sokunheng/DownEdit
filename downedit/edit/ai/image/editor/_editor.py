from downedit.edit.base import Editor


class AIImageEditor(Editor):
    def __init__(self, input_path = "", output_path = ""):
        super().__init__(input_path, output_path)
        self._img = None