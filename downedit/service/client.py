import asyncio
import httpx

class Client:
    def __init__(
        self,
        proxies: dict = None,
        max_retries: int = 5,
        max_connections: int = 10,
        timeout: int = 10,
        max_tasks: int = 10,
        headers: dict = None,
    ):
        self.proxies = proxies if proxies else {}
        self.headers = headers if headers else {}
        self.max_tasks = max_tasks
        self.semaphore = asyncio.Semaphore(max_tasks)
        self.max_connections = max_connections
        self.timeout = timeout
        self.max_retries = max_retries

        self.limits = httpx.Limits(max_connections=self.max_connections)
        self.timeout_config = httpx.Timeout(self.timeout)
        self.transport = httpx.AsyncHTTPTransport(retries=self.max_retries)

    @property
    def aclient(self):
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(
                headers=self.headers,
                proxies=self.proxies,
                verify=False,
                timeout=self.timeout_config,
                limits=self.limits,
                transport=self.transport,
            )
        return self._aclient

    @property
    def client(self):
        if self._client is None:
            self._client = httpx.Client(
                headers=self.headers,
                proxies=self.proxies,
                verify=False,
                timeout=self.timeout_config,
                limits=self.limits,
                transport=self.transport,
            )

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        """
        Async context manager.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Close the client when exiting the context manager.
        """
        await self.client.aclose()
