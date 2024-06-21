import asyncio
import os

from ..base import Task
from ...utils.file_utils import FileUtil
from ...utils.console import Console as console
from ...utils.console import Column as column

class ImageTask(Task):
    """
    Task to be performed on image editor based on the selected operation.
    """
    def __init__(self):
        self.img_tasks = []
        self.task_progress = console().progress_bar(
            column_config=column().edit()
        )
    
    async def add_task(
        self,
        operation,
        image_id,
        output_folder
    ) -> None:
        """
        Adds a task to the queue and updates the progress bar.

        Args:
            operation: The asynchronous function to perform the image edit.
            image_id: The identifier for the image.
            output_folder: The folder to save the edited image.
        """
        file_info = FileUtil.get_file_info(image_id)
        file_name, file_extension, file_size = file_info
        full_file = f"{file_name}{file_extension}"
        output_file_path = FileUtil.get_output_file(
            output_folder,
            full_file,
            file_extension
        )
        units_done = (
            file_size
            if os.path.exists(output_file_path)
            else (os.path.getsize(output_file_path) if os.path.isfile(output_file_path) else 0)
        )
        task_id = await self.task_progress.add_task(
            description="Edit",
            total_units=file_size,
            units_done=units_done,
            file_name=FileUtil.trim_filename(full_file, 40),
            current_state="starting"
        )
        if units_done == file_size:
            await self.task_progress.update_task(task_id, state="completed")
        else:
            edit_task = asyncio.create_task(operation)
            self.img_tasks.append(edit_task)
        
    async def execute(self):
        """
        Executes all queued image editing tasks concurrently.
        """
        await asyncio.gather(*self.img_tasks)
    
    async def close(self):
        """
        Clears the list of queued tasks.
        """
        self.img_tasks.clear()