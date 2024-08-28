import asyncio

from downedit.service.client import Client
from downedit.utils import (
    console,
    column
)


class BaseDownloader(Client):
    """
    Base class for downloading files.
    """

    def __init__(self, kwargs: dict = ...):
        super().__init__()

        self.download_tasks = []
        self.task_progress = console().progress_bar(
            column_config=column().download()
        )


    async def execute(self):
        """
        Executes all queued sound editing tasks concurrently.
        """
        await asyncio.gather(*self.download_tasks)

    async def close(self):
        """
        Clears the list of queued tasks.
        """
        self.download_tasks.clear()

    async def __aenter__(self):
        """
        Enter the context manager
        """
        self.task_progress.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager
        """
        self.task_progress.__exit__(exc_type, exc_val, exc_tb)