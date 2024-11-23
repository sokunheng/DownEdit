

from downedit.utils import (
    ResourceUtil,
    Observer,
    log
)

# /live_api/profile/public?count=9999&pcursor=&principalId={tbUid.Text}&hasMore=true

class KuaiShou:
    def __init__(self, user, **kwargs):
        self.user = user

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
        pass

