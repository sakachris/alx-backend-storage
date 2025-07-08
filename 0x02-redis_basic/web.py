#!/usr/bin/env python3
"""This module defines get_page to fetch and cache web pages with Redis."""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(fn: Callable) -> Callable:
    """
    Decorator to cache the output of get_page and track access count.

    Cache is stored with a TTL of 10 seconds under key 'cache:{url}'.
    Access count is incremented under 'count:{url}'.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapped function that uses Redis to cache and count accesses."""
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        # Check if result is cached
        cached = redis_client.get(cache_key)
        if cached:
            return cached.decode('utf-8')

        # If not cached, increment count and fetch
        redis_client.incr(count_key)
        result = fn(url)
        redis_client.setex(cache_key, 10, result)
        return result

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL using HTTP GET.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the response.
    """
    response = requests.get(url)
    return response.text
