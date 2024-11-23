

from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)


class KuaiShou:
    def __init__(self, user, **kwargs):
        self.user = user

    def _get_output_folder(self) -> str:
        """
        Gets the output folder path for youtube video.
        """
        return ResourceUtil.create_folder(
            folder_type="YOUTUBE"
        )

    def dpwnload(self, video_url: str, video_name: str = "starting..."):
        """
        Downloads the video from the provided URL.
        """
        pass

    def download_all_videos(self):
        """
        Download all videos from the user
        """
        pass

