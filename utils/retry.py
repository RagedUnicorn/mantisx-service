import time
import logging
from functools import wraps
from typing import Tuple, Type, Callable, Any
import requests


def retry_with_backoff(
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (requests.RequestException,),
    status_codes: Tuple[int, ...] = (500, 502, 503, 504)
) -> Callable:
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor to calculate sleep time between retries (exponential)
        exceptions: Tuple of exceptions to catch and retry on
        status_codes: HTTP status codes that should trigger a retry

    Returns:
        Decorated function that implements retry logic
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)

                    # Check if it's a requests.Response object with a retryable status code
                    if hasattr(result, 'status_code') and result.status_code in status_codes:
                        if attempt < max_retries:
                            sleep_time = backoff_factor * (2 ** attempt)
                            logging.warning(
                                f"HTTP {result.status_code} received, retrying in {sleep_time}s... "
                                f"(attempt {attempt + 1}/{max_retries + 1})"
                            )
                            time.sleep(sleep_time)
                            continue

                    return result

                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        sleep_time = backoff_factor * (2 ** attempt)
                        logging.warning(
                            f"{type(e).__name__}: {str(e)}, retrying in {sleep_time}s... "
                            f"(attempt {attempt + 1}/{max_retries + 1})"
                        )
                        time.sleep(sleep_time)
                    else:
                        logging.error(
                            f"Max retries ({max_retries}) exceeded. Last error: {type(e).__name__}: {str(e)}"
                        )
                        raise

            if last_exception:
                raise last_exception

        return wrapper
    return decorator
