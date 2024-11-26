import httpx

from downedit.site.kuaishou.client import KuaiShouClient
from downedit.site.domain import Domain
from downedit.service import retry, httpx_capture
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)
from downedit.utils import (
    log
)

class KuaishouCrawler:
    def __init__(self, *args, **kwargs):
        self.ks_client = KuaiShouClient()
        self.cookies = kwargs.get("cookies", "")
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

    @httpx_capture
    @retry(
        num_retries=3,
        delay=1,
        exceptions=(
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
        ),
    )
    async def __crawl_user_videos(self, principalId: str, pcursor: str = "", cookies: str = ""):
        """
        Crawls the user information.
        """

        header = self.headers.get()
        header["Accept"] = "application/json, text/plain, */*"
        header["Connection"] = "keep-alive"
        # cookies = await self.ks_client.get_client_details()
        # get cookies from class
        header["Cookie"] = self.cookies
        header["Host"] = "live.kuaishou.com"
        header["Referer"] = Domain.KUAI_SHOU.PROFILE_URL + principalId

        response = await Client().aclient.get(
            url=Domain.KUAI_SHOU.PUBLIC_PROFILE,
            headers=header,
            params = {
                "count": 12,
                "pcursor": pcursor,
                "principalId": principalId,
                "hasMore": "true"
            }
        )

        response.raise_for_status()
        json_response = response.json()
        data = json_response.get("data", {})

        return {
            "result": data.get("result", 0),
            "pcursor": data.get("pcursor", ""),
            "videos": data.get("list", [])
        }

    async def fetch_user_videos(self, user_id: str):
        """
        Public method to fetch user videos iteratively.

        Args:
            user_id (str): The user's unique ID for Kuaishou.

        Yields:
            dict: A video metadata for the user.
        """
        try:
            pcursor = ""
            has_more = True

            while has_more:
                user_videos_data = await self.__crawl_user_videos(
                    principalId=user_id,
                    pcursor=pcursor
                )
                for video in user_videos_data.get("videos", []):
                    yield video
                pcursor = user_videos_data.get("pcursor", "")
                has_more = user_videos_data.get("result", 0) == 1 or pcursor == "no_more"

        except Exception as e:
            log.error(f"Error fetching videos for user {user_id}: {str(e)}")
            log.pause()