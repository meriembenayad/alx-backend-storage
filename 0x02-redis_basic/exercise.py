#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """ Cache class """

    def __init__(self):
        """
        Store an instance of the Redis client as a private variable _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key (e.g. using uuid)
        Store the input data in Redis using a random key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
