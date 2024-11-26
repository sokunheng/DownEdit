import asyncio
import secrets
import traceback
import re

from downedit.site.kuaishou._dl import KuaishouDL
from downedit.site.kuaishou.crawler import KuaishouCrawler
from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

class KuaiShou:
    def __init__(self, user, **kwargs):
        self.user = user
        self.cookies = kwargs.get("cookies", "")
        self.observer = Observer()
        self._output_folder = self._get_output_folder()
        self.kuaishou_crawler = KuaishouCrawler(cookies=self.cookies)
        self.kuaishou_dl = KuaishouDL(
            output_folder=self._output_folder
        )

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for KUAISHOU video.
        """
        return ResourceUtil.create_folder(
            folder_type="KUAISHOU"
        )

    def extract_user_id(self, input_string: str) -> str:
        """
        Extracts the user ID from a KuaiShou profile URL or direct user ID input.

        Args:
            input_string (str): The input string, which can be a KuaiShou profile URL or a user ID.

        Returns:
            str: The extracted user ID, or an empty string if no valid ID is found.
        """
        user_id_pattern = r"(?:https?://(?:www|live)\.kuaishou\.com/profile/)?([a-zA-Z0-9]+)"
        match = re.match(user_id_pattern, input_string.strip())
        return match.group(1) if match else ""

    def extract_url_segment(self, url: str) -> str:
        """
        Extracts the specific part of the URL and converts the slashes to underscores.

        Args:
            url (str): The input URL to extract the segment from.

        Returns:
            str: The extracted and converted segment.
        """
        pattern = r"/upic/([\d/]+/[a-zA-Z0-9_]+)"
        match = re.search(pattern, url)

        if match:
            extracted_part = match.group(1)
            converted_part = extracted_part.replace("/", "_")
            return converted_part
        else:
            return secrets.token_hex(16)

    async def download(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.
        """
        try:
            await self.kuaishou_dl.download_video(
                video_url = video_url,
                video_name = video_name
            )
        except Exception as e:
            log.error(traceback.format_exc())
            log.pause()

    async def download_all_videos_async(self):
        """
        Asynchronously downloads all videos from the user.
        """
        user_id = self.extract_user_id(self.user)
        async for video in self.kuaishou_crawler.fetch_user_videos(user_id):
            if self.observer.is_termination_signaled():
                    break

            await self.download(
                video_url=video["playUrl"],
                video_name=self.extract_url_segment(video["playUrl"])
            )

    def download_all_videos(self):
        """
        Download all videos from the user
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(
                self.download_all_videos_async()
            )
        except Exception as e:
            log.error(traceback.format_exc())

