import asyncio
import httpx

class AsyncClient:
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
        
        self._init_client()

    def _init_client(self):
        limits = httpx.Limits(max_connections=self.max_connections)
        timeout_config = httpx.Timeout(self.timeout)
        transport = httpx.AsyncHTTPTransport(retries=self.max_retries)

        self.client = httpx.AsyncClient(
            headers=self.headers,
            proxies=self.proxies,
            timeout=timeout_config,
            limits=limits,
            transport=transport,
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
