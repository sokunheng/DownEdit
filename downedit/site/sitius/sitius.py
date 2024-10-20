import httpx
import asyncio

from downedit import AIContext
from downedit.service import Client
from downedit.site import Domain
from downedit.utils import (
    log
)

class Sitius:
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context

    async def request_job(self):
        try:
            model = self.context.get("model")
            cfg_scale = self.context.get("cfg_scale")
            steps = self.context.get("steps")
            sampler = self.context.get("sampler")

            if not model: self.context.load({"model": "StableDiffusion_v1.4"})
            if not cfg_scale: self.context.load({"cfg_scale": 7})
            if not steps: self.context.load({"steps": 28})
            if not sampler: self.context.load({"sampler": "DPM++ 2M Karras"})
            if not self.service.headers.get("auth"): self.service.headers.update({"auth": "test"})

            request_method = "POST"
            request_headers = self.service.headers
            request_proxies = self.service.proxies

            async with self.service.semaphore:
                content_request = self.service.aclient.build_request(
                    method=request_method,
                    url=Domain.SITIUS.GENERATE,
                    headers=request_headers,
                    timeout=self.service.timeout,
                    json=self.context.json()
                )
                response = await self.service.aclient.send(
                    request=content_request
                )
                
                response.raise_for_status()
                return response.json()

        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
            Exception
        ) as e:
            log.error(f"Error during job request: {e}")
            return None

    async def poll_status(self, job_id, retry_interval=3, max_retries=20):
        """
        Poll the server to check if the image generation is completed.
        """
        for attempt in range(max_retries):
            try:
                response = await self.service.aclient.get(
                    url=f"{Domain.SITIUS.IMAGE}/{job_id}",
                    follow_redirects=True
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    await asyncio.sleep(retry_interval)

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
                httpx.HTTPStatusError,
                httpx.ProxyError,
                httpx.UnsupportedProtocol,
                httpx.StreamError,
                Exception
            ) as e:
                log.error(f"Error while fetching image: {e}")
        return None

    async def generate_image(self):
        """
        Generate an image using the Sitius API.

        Returns:
            str: The URL of the generated image.
        """
        job_id = await self.request_job()
        if not job_id: return None

        image_url = await self.poll_status(job_id)
        if not image_url: return None
        return image_url