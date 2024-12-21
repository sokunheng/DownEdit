import random
import httpx
import asyncio
import random

from random import uniform

from downedit import AIContext
from downedit.service import Client
from downedit.service import retry, httpx_capture
from downedit.site import Domain, Turnstile
from downedit.utils import (
    log
)

class Perchance:
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context
        self.context.load({
            "userKey": "",
            "adAccessCode": "",
            "requestId": "",
            "__cacheBust": ""
        })
        self._thread = 0

    async def refresh_key(self) -> None:
        """
        Verify and refresh the user key if needed.
        """
        if not self.context.get("userKey") or not await self._verify_key(
            self.context.get("userKey")
        ):
            await self._fetch_key()

    async def _fetch_key(self) -> str:
        """
        Fetch a new user key.
        """
        try:
            turnstile= Turnstile(
                header=self.service.headers,
                # proxy=self.service.proxies
                proxy=None
            )
            cloudflare = await turnstile.solve(
                url=Domain.AI_IMAGE.PERCHANCE.EMBED_TURNSTILE,
                sitekey="0x4AAAAAAAA8g8NphwaSOT59"
            )
            solved_token = cloudflare.result
            verify_success = await self._verify_token(solved_token)

            if verify_success:
                return self.context.get("userKey")
            else:
                raise Exception("Turnstile verification failed.")

        except Exception as e:
            print(f"Turnstile or token error: {e}")
            return ""

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
    async def _verify_token(self, token: str) -> bool:
        """
        Verify cloudflare token.

        Args:
            token (str): The cloudflare token.
        """
        response = await self.service.aclient.get(
            url=Domain.AI_IMAGE.PERCHANCE.USER_VERIFY,
            params={
                'token': token,
                'thread': self._thread,
                "__cacheBust": uniform()
            },
            follow_redirects=True
        )
        data = response.json()
        if data["status"] in ("success", "already_verified"):
            self.context.set("userKey", data["userKey"])
            return True
        response.raise_for_status()

    async def _verify_key(self, key: str) -> bool:
        """
        Verify an user key.

        Args:
            key (str): The user key.
        """
        try:
            response = await self.service.aclient.get(
                url=Domain.AI_IMAGE.PERCHANCE.CHECK_VERYIFY,
                params={
                    'userKey': key,
                    '__cacheBust': uniform()
                },
                follow_redirects=True
            )
            if 'not_verified' not in response.json().get('status', ''):
                return True
            response.raise_for_status()
        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
            httpx.ProxyError,
            httpx.UnsupportedProtocol,
            httpx.StreamError,
            Exception
        ) as e:
            return False

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
    async def _verify_user(self):
        """
        Handles user verification, including Turnstile solving if necessary.
        """
        response = await self.service.aclient.get(
            url=Domain.AI_IMAGE.PERCHANCE.USER_VERIFY,
            params={
                'thread': self._thread,
                '__cacheBust': uniform()
            },
            follow_redirects=True
        )
        data = response.json()
        if data["status"] in ("success", "already_verified"):
            self.context.set("userKey", data["userKey"])
            return True
        response.raise_for_status()

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
    async def _get_ad_access_code(self):
        """
        Retrieves and caches the ad access code.
        """
        response = await self.service.aclient.get(
            url=Domain.AI_IMAGE.PERCHANCE.ACCESS_CODE,
            params={
                '__cacheBust': uniform()
            },
            follow_redirects=True
        )
        if response.status_code == 200:
            self.context.set("adAccessCode", response.text)
            return True
        response.raise_for_status()

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
    async def generate(self):
        """
        Generates an image using the Perchance API.
        """
        await self.refresh_key()

        if not self.context.get("adAccessCode"):
            await self._get_ad_access_code()

        self.context.set("requestId", uniform())
        self.context.set("__cacheBust", uniform())

        request_method = "POST"
        request_headers = self.service.headers
        request_proxies = self.service.proxies

        async with self.service.semaphore:
            content_request = self.service.aclient.build_request(
                method=request_method,
                url=Domain.AI_IMAGE.PERCHANCE.GENERATE_IMAGE,
                headers=request_headers,
                timeout=self.service.timeout,
                json=self.context.json()
            )
            response = await self.service.aclient.send(
                request=content_request
            )

        if response.status_code == 200:
            return response.json()
        else:
            await self.refresh_key()


class PerchanceCC:
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context

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
    async def generate(self):
        """
        Generates an image using the Perchance API.
        """
        request_method = "POST"
        request_headers = self.service.headers
        request_proxies = self.service.proxies
        self.service.timeout = 18

        async with self.service.semaphore:
            content_request = self.service.aclient.build_request(
                method=request_method,
                url=Domain.AI_IMAGE.PERCHANCE.PREDICT,
                headers=request_headers,
                timeout=self.service.timeout,
                json=self.context.json()
            )
            response = await self.service.aclient.send(
                request=content_request,
                follow_redirects=True
            )

            if not response.text.strip() or not response.content:
                await asyncio.sleep(0.5)

            response.raise_for_status()
            return response.json()


class AIGG:
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context
        _size_value = self.context.get("size")
        self.extract_dimensions(_size_value)
        self.context.set("quantity", 1)

    def extract_dimensions(self, size_value):
        """
        Extract width and height from the size value.
        """
        if 'x' in size_value:
            width, height = map(int, size_value.split('x'))
        else:
            width = 512
            height = int(size_value)

        self.context.set("width", width)
        self.context.set("height", height)

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
    async def generate(self):
        """
        Generates an image using the AIGG API.
        """
        request_method = "POST"
        request_headers = self.service.headers
        request_proxies = self.service.proxies
        self.service.timeout = 18

        async with self.service.semaphore:
            content_request = self.service.aclient.build_request(
                method=request_method,
                url=Domain.AI_IMAGE.AIGG.GENERATE_IMAGE,
                headers=request_headers,
                timeout=self.service.timeout,
                json=self.context.json()
            )

            response = await self.service.aclient.send(
                request=content_request,
                follow_redirects=True
            )

            if not response.text.strip() or not response.content:
                await asyncio.sleep(0.5)

            response.raise_for_status()
            return response.json()


class DE_AI_GENERATOR:
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context
        self.providers = self._get_providers()

    def _get_providers(self):
        """
        Returns a list of AI image providers.
        """
        # provider_classes = [Perchance, PerchanceCC, AIGG]
        provider_classes = [PerchanceCC, AIGG]
        selected_provider = random.choice(provider_classes)

        prov_arg = {}
        prov_arg["key"] = "RANDOM"
        prov_arg["size"] = self.context.get("size", "512x512")
        prov_arg["prompt"] = self.context.get("prompt")
        prov_arg["negativePrompt"] = self.context.get("negativePrompt")
        self.context.reset(prov_arg)
        return selected_provider(self.service, self.context)

    async def generate(self):
        """
        Generates an image using a selected provider.
        """
        return await self.providers.generate()
