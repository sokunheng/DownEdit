import asyncio
import time

from typing import Generator, List
from itertools import islice

from downedit.edit.ai.local.image.editor import AIImageOperation
from downedit.edit.image import ImageOperation
from downedit.edit.sound import SoundOperation
from downedit.edit.video import VideoOperation
from downedit.edit.base import (
    Editor,
    Handler,
    Task
)
from downedit.utils import (
    Observer,
    ResourceUtil,
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
        self._process_folder = process_folder
        # self._input_folder = None
        self._output_folder = self._get_output_folder(tool)
        self._operations = self._init_operations(**kwargs)

        # Initialize task based on media type
        self._task = self._get_task()

    def _generate_file_paths(self, process_folder:str) -> Generator[str, None, None]:
        """
        Gets a generator of individual file paths (to be implemented by subclasses).
        """
        raise NotImplementedError

    def _get_input_files(self, process_folder: str, batch_size: int = 5) -> Generator[List[str], None, None]:
        """
        Generates batches of input file paths from the given folder.

        Args:
            process_folder (str): The folder containing files to process.
            batch_size (int): Number of files per batch. Defaults to 5.

        Yields:
            List[str]: A list of file paths in each batch.
        """
        file_paths_generator = iter(self._generate_file_paths(process_folder))
        return (
            list(batch) for batch in iter(
                lambda: tuple(islice(file_paths_generator, batch_size)), ()
            )
        )

    def _get_output_folder(self, tool: str) -> str:
        """
        Gets the output folder path based on the tool and media type.
        """
        raise NotImplementedError

    def _get_output_files(self) -> List[str]:
        """
        Gets the list of output files based on the media type.
        """
        return ResourceUtil.get_file_list(
            directory=self._output_folder
        )

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
        if isinstance(operations, (
            ImageOperation,
            SoundOperation,
            VideoOperation,
            AIImageOperation
        )):
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
            editor: Editor = self._create_editor(media_path)
            output_suffix = self._build_and_apply_operations(editor, "")

            # Get file info for output file path construction
            file_info = ResourceUtil.get_file_info(media_path)
            file_name, file_extension, file_size = file_info

            # Construct the output file path
            full_file = f"{file_name}{output_suffix}"
            output_file_path = ResourceUtil.get_output_file(
                self._output_folder,
                full_file,
                file_extension
            )
            editor.output_path = output_file_path

            # Add the task to the task queue
            await self._task.add_task(
                operation_function= await editor.render(**render_kwargs),
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
        start_time = time.time()
        proceed_count = 0

        for batch in self._get_input_files(self._process_folder):
            if self.observer.is_termination_signaled():
                break

            await self._task.init_progress()

            for media_path in batch:
                if self.observer.is_termination_signaled():
                    break
                if await self._process_media(media_path, **render_kwargs):
                    proceed_count += 1

            await self._task.execute()
            await self._task.end_progress()
            await self._task.close()

        elapsed_time = time.time() - start_time

        log.info(f"Processed: {elapsed_time:.2f} seconds.")
        log.file(f"Saved at [green]{self._output_folder}[/green]")
        log.file(f"Processed [green]{proceed_count}[/green] media files successfully.")
        # log.file(f"Processed [green]{len(self._get_output_files())}[/green] media files successfully.")
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