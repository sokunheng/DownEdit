import asyncio
import os

from downedit.download import Downloader
from downedit.edit.base import Task
from downedit.utils import (
    ResourceUtil
)
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)

class AIImgGenTask(Task):
    """
    Task to be performed on image generation based on the selected provider.
    """
    def __init__(self) -> None:
        self.user_agent = UserAgent(
            platform_type='mobile',
            device_type='android',
            browser_type='chrome'
        )
        self.client_hints = ClientHints(self.user_agent)
        self.headers = Headers(self.user_agent, self.client_hints)
        self.headers.accept_ch("""
            sec-ch-ua,
            sec-ch-ua-full-version-list,
            sec-ch-ua-platform,
            sec-ch-ua-platform-version,
            sec-ch-ua-mobile,
            sec-ch-ua-bitness,
            sec-ch-ua-arch,
            sec-ch-ua-model,
            sec-ch-ua-wow64
        """)
        self.client = Client(headers=self.headers.get())
        self.task_progress = Downloader(self.client)

    async def add_task(
        self,
        operation_url,
        operation_media,
    ) -> None:
        """
        Adds a task to the queue and updates the progress bar.

        Args:
            operation_url: The URL of the image to be generated.
            operation_media: The identifier for the image.
        """
        await self.task_progress.add_file(
            file_url=operation_url,
            file_media=operation_media
        )

    async def execute(self):
        """
        Executes all queued image editing tasks concurrently.
        """
        self.task_progress.execute()

    async def close(self):
        """
        Clears the list of queued tasks.
        """
        self.task_progress.close()
        await asyncio.sleep(0.1)