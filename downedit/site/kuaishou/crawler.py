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
    def __init__(self):
        self.ks_client = KuaiShouClient()
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

    async def __crawl_user_videos(self):
        """
        Crawls the user information.
        """
        cookie = await self.ks_client.get_client_details()
        header = self.headers.get()
        header["cookie"] = cookie

        response = await Client().aclient.post(
            url=Domain.KUAI_SHOU.PROFILE_URL,
            headers=header,
        )

        response.raise_for_status()
        return response.json()