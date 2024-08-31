import asyncio
import os
from typing import Any

import aiofiles
import httpx

from downedit.service import Client
from downedit.utils import (
    console,
    column,
    FileUtil,
    log
)

class Downloader():
    """
    Base class for downloading files.
    """

    def __init__(self, service: Client):
        self.service = service
        self.download_tasks = []
        self.task_progress = console().progress_bar(
            column_config=column().download()
        )

    def _get_chunk_size(self, file_size: int) -> int:
        """
        Determines the chunk size for downloading a file based on its size.

        Args:
            file_size (int): The size of the file in bytes.

        Returns:
            int: The chunk size in bytes.
        """
        chunk_sizes = [
            (10 * 1024, 64 * 1024),
            (1 * 1024 * 1024, 256 * 1024),
            (10 * 1024 * 1024, 1 * 1024 * 1024),
            (100 * 1024 * 1024, 10 * 1024 * 1024)
        ]
        default_chunk_size = 5 * 1024 * 1024

        for limit, size in chunk_sizes:
            if file_size < limit:
                return size

        return default_chunk_size

    async def _get_content(
        self,
        content_url: str,
        headers: dict = ...,
        proxy_url: str = None
    ) -> int:
        """
        (Retrieve the Content-Length for a given URL)

        Args:
            url (str): (Target URL)
            headers (dict): (Request headers)
            proxies (dict): (Proxies)

        Returns:
            int: (Value of Content-Length, or 0 if retrieval fails)
        """
        async with httpx.AsyncClient(
            timeout=10.0,
            transport=httpx.AsyncHTTPTransport(retries=5, proxy=proxy_url),
            verify=False,
        ) as aclient:
            try:
                response = await aclient.head(
                    url=content_url,
                    headers=headers,
                    follow_redirects=True
                )
                if int(response.headers.get("Content-Length", 0)) == 0:
                    response = await aclient.get(
                        url=content_url,
                        headers=headers,
                        follow_redirects=True
                    )
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in [405, 403, 401, 302]:
                    try:
                        response = await aclient.get(
                            url=content_url,
                            headers=headers,
                            follow_redirects=True,
                            stream=True
                        )
                        response.raise_for_status()
                    except Exception as e:
                        log.error(e)
                        return 0
                else:
                    log.error(e)
                    return 0

            except (httpx.ConnectTimeout, httpx.RequestError) as e:
                log.error(f"Unable to request: {e}")
                return 0

            except Exception as e:
                log.error(f"Unable to retrieving content")
                return 0

            return int(response.headers.get("Content-Length", 0))

    async def add_file(
        self,
        file_url: str,
        file_media: Any,
        service_step: tuple =("Download", "Downloading", "Downloaded"),
    ):
        """
        Adds a task to the queue and updates the progress bar.

        Args:
            file_url: The URL of the file to download.
            file_media: The identifier for the media.
        """
        file_output, file_name = file_media
        start_step, _, _ = service_step
        task_id = await self.task_progress.add_task(
            description=start_step,
            file_name=FileUtil.trim_filename(file_name, 40).ljust(40),
            current_state="idle"
        )

        if os.path.exists(file_output):
            log.critical(f"{FileUtil.trim_filename(file_name, 40)} already exists! Skipping...")
            return await self.task_progress.update_task(
                task_id,
                new_state="success"
            )

        await self.task_progress.update_task(
            task_id,
            new_state="starting"
        )

        download_task = asyncio.create_task(
            self.download_file(
                service_step,
                task_id,
                file_url,
                file_output
            )
        )
        self.download_tasks.append(download_task)

    async def download_file(
        self,
        seveice_step: tuple,
        task_id,
        file_url: Any,
        file_output: Any
    ):
        """
        Saves the file to the specified path.

        Args:
            task_id: The identifier for the task.
            file_url: The content of the file to save.
            file_output: The path to save the file to.
        """
        _, working_step, end_step = seveice_step
        request_method = "GET"
        request_headers = self.service.headers
        request_proxies = self.service.proxies

        async with self.service.semaphore:
            content_length = await self._get_content(
                file_url,
                request_headers,
                request_proxies,
            )

            if content_length == 0:
                return await self.task_progress.update_task(
                    task_id,
                    new_state="failure"
                )

            await self.task_progress.update_task(
                task_id,
                new_total=int(content_length)
            )

            async with aiofiles.open(
                file=file_output,
                mode="wb"
            ) as file:
                try:
                    # content_request = self.service.aclient.build_request(
                    #     method=request_method,
                    #     url=file_url,
                    #     headers=request_headers,
                    #     timeout=self.service.timeout
                    # )
                    # file_bytes = await self.service.aclient.send(
                    #     request=content_request,
                    #     stream=True
                    # )
                    async with self.service.aclient.stream(
                        method=request_method,
                        url=file_url,
                        headers=request_headers,
                        timeout=self.service.timeout
                    ) as file_bytes:
                        async for chunk in file_bytes.aiter_bytes(
                            self._get_chunk_size(content_length)
                        ):
                            await file.write(chunk)
                            await self.task_progress.update_task(
                                task_id,
                                progress_increment=len(chunk)
                            )
                except (
                    httpx.TimeoutException,
                    httpx.NetworkError,
                    httpx.HTTPStatusError,
                    httpx.ProxyError,
                    httpx.UnsupportedProtocol,
                    httpx.StreamError,
                    Exception
                ) as e:
                    log.error(f"Error during {working_step}: {e}")
                    return await self.task_progress.update_task(
                        task_id,
                        new_state="failure"
                    )

        log.info(f"{end_step}: {file_output}")
        await self.task_progress.update_task(
            task_id,
            new_state="success"
        )

    async def execute(self):
        """
        Executes all queued sound editing tasks concurrently.
        """
        await asyncio.gather(*self.download_tasks)

    async def close(self):
        """
        Clears the list of queued tasks.
        """
        self.download_tasks.clear()
        if self.service.client: self.service.client.close()
        if self.service.aclient: await self.service.aclient.aclose()

    async def __aenter__(self):
        """
        Enter the context manager
        """
        self.task_progress.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager
        """
        self.task_progress.__exit__(exc_type, exc_val, exc_tb)
        await self.close()
