#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


""" 2. Incrementing values """


def count_calls(method: Callable) -> Callable:
    """ Decorator """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """ Cache class """

    def __init__(self):
        """
        Store an instance of the Redis client as a private variable _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    """ 2. Incrementing values """
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key (e.g. using uuid)
        Store the input data in Redis using a random key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    """ 1. Reading from Redis and recovering original type """

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Get data from Redis using the key
        Convert the key using the Callable
        """
        storedKey = self._redis.get(key)
        if fn is not None and storedKey is not None:
            return fn(storedKey)
        return storedKey

    def get_str(self, key: str) -> str:
        """
        Get data from Redis using the key
        Convert it to string
        """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """
        Get data from Redis using the key
        Convert it to int
        """
        return self.get(key, fn=int)
