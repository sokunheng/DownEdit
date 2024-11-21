import asyncio
import os

from downedit.download import Downloader
from downedit.edit.base import Task
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

    async def execute(self, operation_url: str, operation_media: tuple):
        """
        Starts the task for downloading

        Args:
            video_url (str): The URL of the iamge to download.
            operation_media (tuple): The media file information.
        """
        client = Client(headers=self.headers.get())

        async with Downloader(client) as downloader:
            await downloader.add_file(
                file_url=operation_url,
                file_media=operation_media
            )
            await downloader.execute()
            await downloader.close()

    async def close(self) -> None:
        pass