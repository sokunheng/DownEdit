import secrets
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
            platform_type="desktop",
            device_type="windows",
            browser_type="chrome"
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

    def generate_web_did(self):
        """
        Generates a 'did' cookie value in the format:
        'web_<32-character-hex-string>'.

        Returns:
            str: A generated 'did' value.
        """
        return f"web_{secrets.token_hex(16)}"

    def extract_cookie_value(self, cookies, cookie_name):
        """
        Extracts the value of a specific cookie from a CookieJar object.

        Args:
            cookies (CookieJar): The cookies object returned from the HTTP response.
            cookie_name (str): The name of the cookie to extract.

        Returns:
            str: The value of the specified cookie, or an empty string if not found.
        """
        cookie = next((cookie.value for cookie in cookies.jar if cookie.name == cookie_name), "")
        return cookie

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
        headers = self.headers.get()
        headers["Accept"] = "*/*"
        headers["Connection"] = "keep-alive"
        headers["Host"] = "live.kuaishou.com"
        headers["Referer"] = Domain.KUAI_SHOU.DOMAIN

        response = await self.client.aclient.get(
            url=Domain.KUAI_SHOU.POPULAR,
            headers=headers,
            follow_redirects=True
        )
        response.raise_for_status()
        # json_response = response.json()
        did_cookies = response.cookies.get("did", "")
        _did_cookies = response.cookies.get("_did", "")
        live_bfb1s_cookies = response.cookies.get("kuaishou.live.bfb1s", "")
        clientid_cookies = response.cookies.get("clientid", "")
        client_key_cookies = response.cookies.get("client_key", "")
        kpn_cookies = response.cookies.get("kpn", "")
        client_cookies = (
            # f"_did={_did_cookies};"
            f"did={did_cookies}; ",
            f"kuaishou.live.bfb1s={live_bfb1s_cookies}; "
            f"clientid={clientid_cookies}; ",
            f"did={did_cookies}; ",
            f"client_key={client_key_cookies}; ",
            f"kpn={kpn_cookies}",
        )
        return "".join(client_cookies)
