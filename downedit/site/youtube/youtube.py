import asyncio
import traceback

from downedit.site.domain import Domain
from downedit.site.youtube._download import YoutubeDL
from downedit.site.youtube.crawler import YouTubeCrawler
from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

class Youtube:
    def __init__(self, channel, **kwargs):
        self.channel = channel
        self.video_type = kwargs.get("video_type", "videos")
        self.observer = Observer()
        self._output_folder = self._get_output_folder()
        self.youtube_crawler = YouTubeCrawler()
        self.youtube_dl = YoutubeDL(
            output_folder=self._output_folder
        )

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for youtube video.
        """
        return ResourceUtil.create_folder(
            folder_type="YOUTUBE"
        )

    async def download_all_videos_async(self):
        """
        Download all videos from the channel asynchronously
        """
        async for video in self.youtube_crawler.aget_channel(
            channel_url=self.channel,
            content_type=self.video_type
        ):
            if self.observer.is_termination_signaled():
                    break

            await self.youtube_dl.download_video(
                video_url = video["videoId"],
                # video_name = video["title"]["accessibility"]["accessibilityData"]["label"]
                video_name = video["title"]["runs"][0]["text"]
            )

    def download_all_videos(self):
        """
        Download all videos from the channel
        """
        self.observer.register_termination_handlers()
        try:
            asyncio.run(
                self.download_all_videos_async()
            )
        except Exception as e:
            log.error(traceback.format_exc())
