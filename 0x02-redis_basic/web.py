#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker """
import redis
import requests
from typing import Callable
from functools import wraps


def counts_calls(method: Callable) -> Callable:
    """ Decorator """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper """
        key = f'count: {args[0]}'
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Web:
    """ class Web """

    def __init__(self):
        """ Initialize """
        self._redis = redis.Redis()

    @counts_calls
    def get_page(self, url: str) -> str:
        """
        Obtain the HTML content of a particular URL and returns it.
        """
        # Check if the result is in cache
        result = self._redis.get(url)
        if result is not None:
            return result.decode('utf-8')

        # if it's not in cache
        response = requests.get(url)
        result = response.text

        # Cache the result with expired time of 10 seconds
        self._redis.setex(url, 10, result)

        return result
