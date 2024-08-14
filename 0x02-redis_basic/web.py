import redis
import requests
import time
from typing import Callable

# Initialize the Redis client
redis_client = redis.Redis()


def cache_page(url: str, expiration: int = 10) -> str:
    """
    Fetch the HTML content of a URL, cache the result with an expiration time,
    and track the number of accesses.

    Args:
        url (str): The URL to fetch.
        expiration (int): The expiration time of the cache in seconds.

    Returns:
        str: The HTML content of the URL.
    """
    # Generate the cache key and access count key
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"

    # Check if the URL is cached
    cached_content = redis_client.get(cache_key)
    if cached_content:
        # Increment the access count
        redis_client.incr(count_key)
        return cached_content.decode('utf-8')

    # Fetch the content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the result and set the expiration time
    redis_client.setex(cache_key, expiration, html_content)

    # Increment the access count
    redis_client.incr(count_key)

    return html_content


# Decorator for caching and access tracking
def track_page_access(func: Callable) -> Callable:
    """
    Decorator to track page accesses and cache the results.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    def wrapper(url: str) -> str:
        return func(url)
    return wrapper


# Apply the decorator
@track_page_access
def get_page(url: str) -> str:
    return cache_page(url)
