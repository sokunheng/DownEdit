import httpx

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

class KuaiShouClient:
    """
    KuaiShou client configuration.
    """
    def __init__(self, client: Client = None):
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
        self.default_client = Client(headers=self.headers.get())
        self.client = client or self.default_client

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
    async def get_client_details(self):
        """
        Generates KuaiShou client details.

        Returns:
            dict: A dictionary containing client details.
        """
        response = await self.client.aclient.get(
            url=Domain.KUAI_SHOU.DISCOVERY,
            headers=self.headers.get(),
            follow_redirects=True
        )
        response.raise_for_status()
        return response.cookies