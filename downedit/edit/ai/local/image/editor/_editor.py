import aiofiles

from rembg import remove, new_session
from downedit.edit.base import Editor

class AIImageEditor(Editor):
    def __init__(self, input_path = "", output_path = ""):
        super().__init__(input_path, output_path)
        self._img = None
        self.session = new_session()

    def remove_bg(self):
        with open(self.input_path, 'rb') as i:
            input = i.read()
            self._img = remove(
                input,
                session=self.session,
                force_return_bytes=True
            )
        return self

    async def render(
        self
    ):
        """
        Writes the modified image to the specified output path.
        """
        async with aiofiles.open(
            file=self.output_path,
            mode="wb"
        ) as file:
            await file.write(self._img)