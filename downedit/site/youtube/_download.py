import traceback
import httpx

from typing import Optional, Dict

from downedit.site import Domain
from downedit.site.youtube.client import YoutubeClient
from downedit.download import Downloader
from downedit.service import (
    Client
)
from downedit.utils import (
    ResourceUtil,
    log
)

class YoutubeDL:
    def __init__(self, output_folder: str):
        self.yt_client = YoutubeClient()
        self.output_folder = output_folder

    async def _get_player_response(self, video_id: str) -> Optional[Dict]:
        """
        Gets the player response for the video.

        Args:
            video_id (str): The video identifier.

        Returns:
            dict: A dictionary containing the player response.
        """
        client_details = self.yt_client.get_client_details()
        payload = await self.yt_client.create_payload(video_id)
        headers = await self.yt_client.create_headers(client_details)

        try:
            response = await Client().aclient.post(
                url=Domain.YOUTUBE.YT_PLAYER,
                json=payload,
                headers=headers,
            )

            response.raise_for_status()
            return response.json()

        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
            Exception
        ) as e:
            log.error(traceback.format_exc())
            return None

    async def download_video(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.

        Args:
            video_url (str): The URL of the video to download.
            video_name (str, optional): Defaults to "starting...".
        """
        player_response = await self._get_player_response(video_url)
        if player_response is None:
            log.error("No player response found.")
            return

        video_stream = player_response.get("streamingData", {}).get("adaptiveFormats", [])
        if not video_stream:
            log.error("No video stream found.")
            return

        video_stream = video_stream[0]
        video_url = video_stream.get("url", "")

        output_file = ResourceUtil.get_output_file(
            self.output_folder,
            video_name,
            ".mp4"
        )
        client = Client()
        client.headers["User-Agent"] = self.yt_client.get_client_details()["userAgent"]

        async with Downloader(client) as downloader:
            await downloader.add_file(
                file_url=video_url,
                file_media=(output_file, video_name)
            )
            await downloader.execute()
            await downloader.close()