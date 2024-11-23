import asyncio
import traceback

from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

class KuaiShou:
    def __init__(self, user, **kwargs):
        self.user = user
        self.observer = Observer()

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for KUAISHOU video.
        """
        return ResourceUtil.create_folder(
            folder_type="KUAISHOU"
        )

    def download(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.
        """
        pass

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

