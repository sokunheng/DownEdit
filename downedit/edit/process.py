import asyncio
import time

from typing import List

from downedit.edit.image import ImageOperation
from downedit.edit.sound import SoundOperation
from downedit.edit.video import VideoOperation
from downedit.edit.base import (
    Handler,
    Task
)
from downedit.utils import (
    Observer,
    FileUtil,
    log
)

class Process:
    """
    Base class for processing media files (images, sounds, videos).
    """

    def __init__(
        self,
        tool: str,
        process_folder: str,
        batch_size: int = 5,
        **kwargs
    ) -> None:
        self.observer = Observer()
        self.batch_size = batch_size
        self._tool = tool
        self._input_folder = self._get_input_files(process_folder)
        self._output_folder = self._get_output_folder(tool)
        self._operations = self._init_operations(**kwargs)

        # Initialize task based on media type
        self._task = self._get_task()

    def _get_input_files(self, process_folder: str) -> List[str]:
        """
        Gets the list of input files based on the media type.
        """
        raise NotImplementedError

    def _get_output_folder(self, tool: str) -> str:
        """
        Gets the output folder path based on the tool and media type.
        """
        raise NotImplementedError

    def _init_operations(self, **kwargs) -> Handler:
        """
        Initializes the operations list based on the selected tool.
        """
        raise NotImplementedError

    def _get_task(self) -> Task:
        """
        Gets the appropriate Task object based on the media type.
        """
        raise NotImplementedError

    def _build_and_apply_operations(self, editor, output_suffix: str) -> str:
        """
        Builds and applies the operations to the editor.
        """
        operations = self._operations._get(self._tool)
        if isinstance(operations, (ImageOperation, SoundOperation, VideoOperation)):
            output_suffix = operations.handle(editor, output_suffix)
        elif isinstance(operations, list):
            for operation in operations:
                output_suffix = operation.handle(editor, output_suffix)
        return output_suffix

    async def _process_media(self, media_path: str, **render_kwargs) -> bool:
        """
        Process a single media file.
        """
        try:
            # Create editor object (specific for each media type)
            editor = self._create_editor(media_path)
            output_suffix = self._build_and_apply_operations(editor, "")

            # Get file info for output file path construction
            file_info = FileUtil.get_file_info(media_path)
            file_name, file_extension, file_size = file_info

            # Construct the output file path
            full_file = f"{file_name}{output_suffix}"
            output_file_path = FileUtil.get_output_file(
                self._output_folder,
                full_file,
                file_extension
            )
            editor.output_path = output_file_path

            # Add the task to the task queue
            await self._task.add_task(
                operation_function=lambda: editor.render(**render_kwargs),
                operation_media=(
                    output_file_path,
                    f"{file_name}{file_extension}",
                    file_size
                )
            )
            return True

        except Exception as e:
            log.error(e)
            return False

    async def start_async(self, **render_kwargs):
        """
        Process the media files in the input folder asynchronously.
        """
        proceed_count = 0
        start_time = time.time()

        for start_idx in range(0, len(self._input_folder), self.batch_size):
            if self.observer.is_termination_signaled():
                break

            end_idx = min(start_idx + self.batch_size, len(self._input_folder))
            batch = self._input_folder[start_idx:end_idx]

            for media_path in batch:
                if self.observer.is_termination_signaled():
                    break
                if await self._process_media(media_path, **render_kwargs):
                    proceed_count += 1
                else:
                    continue
            await self._task.execute()
            await self._task.close()

        elapsed_time = time.time() - start_time

        log.info(f"Processed: {elapsed_time:.2f} seconds.")
        log.file(f"Saved at [green]{self._output_folder}[/green]")
        log.file(f"Processed [green]{proceed_count}[/green] media files successfully.")
        log.pause()

    def start(self, **render_kwargs):
        """
        Process the media files in the input folder synchronously.
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(self.start_async(**render_kwargs))
        except Exception as e:
            log.error(e)

    def __enter__(self):
        """
        Set up the context for media processing.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clean up the context after media processing.
        """
        pass