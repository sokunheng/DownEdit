import httpx
import asyncio

from random import random as uniform
from playwright.async_api import async_playwright

from downedit import AIContext
from downedit.service import Client
from downedit.site import Domain
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

    async def _start_playwright(self):
        """
        Lazily starts Playwright.
        """
        if self.__playwright is None:
            self.__playwright = await async_playwright().start()

    async def _solve_turnstile(self, page):
        """
        Solves the Turnstile challenge using Playwright and returns the token.
        """
        await page.wait_for_selector(".cf-turnstile", state="attached")
        token = await page.evaluate(
            """async () => {
                return new Promise((resolve) => {
                    window.turnstile.ready(async (turnstile) => {
                        turnstile.render('#cfTurnstileCtn', {
                            sitekey: '0x4AAAAAAAA8g8NphwaSOT59',
                            callback: (token) => {
                                resolve(token);
                            }
                        });
                    })
                });
            }"""
        )
        return token

    async def refresh_key(self) -> None:
        """
        Verify and refresh the user key if needed.
        """
        if not self._user_key or not await self._verify_key(self._user_key):
            self._user_key = await self._fetch_key()

    async def _fetch_key(self) -> str:
        """
        Fetch a new user key.
        """
        async with async_playwright() as aplaywright:
            try:
                playwright_browser = await aplaywright.firefox.launch(headless=False)
                browser_context = await playwright_browser.new_context(
                    extra_http_headers=self.service.headers
                )
                web_page = await browser_context.new_page()
                await web_page.goto(
                    url=Domain.AI_IMAGE.PERCHANCE.EMBED_TURNSTILE,
                    referer=Domain.AI_IMAGE.PERCHANCE.EMBED_TURNSTILE
                )
                cloudflare_token = await self._solve_turnstile(web_page)
                verify_success = await self._verify_token(cloudflare_token)
                if verify_success:
                    return self.context.get("userKey")
                else:
                    raise Exception("Turnstile verification failed.")

            except Exception as e:
                print(f"Turnstile or token error: {e}")
                return ""

            finally:
                await web_page.close()
                await browser_context.close()

    async def _verify_token(self, token: str) -> bool:
        """
        Verify cloudflare token.

        Args:
            token (str): The cloudflare token.
        """
        try:
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

    async def _verify_user(self):
        """
        Handles user verification, including Turnstile solving if necessary.
        """
        try:
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

    async def _get_ad_access_code(self):
        """
        Retrieves and caches the ad access code.
        """
        try:
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

    async def generate(self):
        """
        Generates an image using the Perchance API.
        """
        await self.refresh_key()

        if not self.context.get("adAccessCode"):
            await self._get_ad_access_code()

        for _ in range(3):
            try:

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
                    await asyncio.sleep(1)
                    await self.refresh_key()

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
                httpx.HTTPStatusError,
                httpx.ProxyError,
                httpx.UnsupportedProtocol,
                httpx.StreamError,
                Exception
            ) as e:
                print(f"Error during job request: {e}")
                return None


class PerchanceCC:
    def __init__(
        self,
        service: Client,
        context: AIContext = AIContext()
    ):
        self.service = service
        self.context = context

    async def generate(self):
        """
        Generates an image using the Perchance API.
        """
        for _ in range(3):
            try:

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
                        request=content_request
                    )

                if response.status_code == 200:
                    return response.json()
                else:
                    await asyncio.sleep(1)

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
                httpx.HTTPStatusError,
                httpx.ProxyError,
                httpx.UnsupportedProtocol,
                httpx.StreamError,
                Exception
            ) as e:
                continue


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

    async def generate(self):
        """
        Generates an image using the AIGG API.
        """
        for _ in range(3):
            try:

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
                        request=content_request
                    )

                if response.status_code == 200:
                    return response.json()
                else:
                    await asyncio.sleep(1)

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
                httpx.HTTPStatusError,
                httpx.ProxyError,
                httpx.UnsupportedProtocol,
                httpx.StreamError,
                Exception
            ) as e:
                continue

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
        provider_classes = [PerchanceCC, AIGG]
        selected_provider = uniform.choice(provider_classes)

        prov_arg = {}
        prov_arg["key"] = "RANDOM"
        prov_arg["size"] = self.context.get("size", "512x512")
        prov_arg["prompt"] = self.context.get("prompt")
        prov_arg["negativePrompt"] = self.context.get("negative_prompt")
        self.context.reset(prov_arg)

        return selected_provider(self.service, self.context)

    async def generate(self):
        """
        Generates an image using a selected provider.
        """
        return await self.providers.generate()
