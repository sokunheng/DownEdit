import asyncio
import random
from functools import wraps

def retry(num_retries=3, delay=1, exceptions=(Exception,)):
    """
    Retry decorator.

    Args:
        num_retries (int, optional): number of retries
        delay (int, optional): delay between retries
        exceptions (tuple, optional): exceptions to catch
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(num_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt < num_retries - 1:
                        await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator
