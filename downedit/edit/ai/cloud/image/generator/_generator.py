from downedit         import AIContext
from downedit.service import (
    Client,
    ClientHints,
    UserAgent,
    Headers
)


class AIImgGenerator:
    def __init__(self, provider, context: str):
        self.user_context = context
        self.ai_context = AIContext()
        self.provider = provider
        self.user_agent = UserAgent(
            platform_type='desktop',
            device_type='windows',
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