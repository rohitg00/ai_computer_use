"""Utility decorators"""

import asyncio
import functools
from typing import Any, Callable, Optional, Type, TypeVar

from .logging import setup_logging

logger = setup_logging()

T = TypeVar('T')

def with_retries(
    retries: int = 3,
    delay: float = 1.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    logger = None
):
    """Retry decorator for async functions"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_error: Optional[Exception] = None
            
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if logger:
                        logger.warning(
                            f"Attempt {attempt + 1}/{retries} failed: {str(e)}"
                        )
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                        
            if last_error:
                raise last_error
                
        return wrapper
    return decorator

def log_execution(logger = None):
    """Log function execution with timing"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            start = asyncio.get_event_loop().time()
            try:
                result = await func(*args, **kwargs)
                elapsed = asyncio.get_event_loop().time() - start
                if logger:
                    logger.debug(
                        f"{func.__name__} completed in {elapsed:.2f}s"
                    )
                return result
            except Exception as e:
                elapsed = asyncio.get_event_loop().time() - start
                if logger:
                    logger.error(
                        f"{func.__name__} failed after {elapsed:.2f}s: {str(e)}"
                    )
                raise
        return wrapper
    return decorator 