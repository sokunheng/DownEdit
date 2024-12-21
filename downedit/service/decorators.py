import asyncio
import traceback
import httpx

from decorator import decorator
from downedit.utils import log

@decorator
async def retry(
    func,
    *args,
    num_retries=3,
    delay=1,
    exceptions=(Exception,),
    **kwargs
):
    """
    Retry decorator.

    Args:
        func (callable): The function to wrap.
        num_retries (int, optional): Number of retries. Defaults to 3.
        delay (int, optional): Delay between retries in seconds. Defaults to 1.
        exceptions (tuple, optional): Exceptions to catch. Defaults to (Exception,).
    """
    for attempt in range(num_retries):
        try:
            result = await func(*args, **kwargs)
            if result is not None:
                return result
        except exceptions as e:
            # log.error(traceback.format_exc())
            if attempt < num_retries - 1:
                await asyncio.sleep(delay)
    return None

@decorator
async def httpx_capture(func, *args, **kwargs):
    """
    Capture error decorator.

    Args:
        func (callable): The function to wrap.
    """
    try:
        return await func(*args, **kwargs)
    except (
        httpx.TimeoutException,
        httpx.NetworkError,
        httpx.HTTPStatusError,
        httpx.ProxyError,
        httpx.UnsupportedProtocol,
        httpx.StreamError,
        Exception,
    ) as e:
        log.error(traceback.format_exc())
        log.pause()
        raise