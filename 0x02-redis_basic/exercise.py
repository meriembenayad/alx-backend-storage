#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


""" 2. Incrementing values """


def count_calls(method: Callable) -> Callable:
    """ Decorator Increments called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


""" 3. Storing lists """


def call_history(method: Callable) -> Callable:
    """ Decorator """
    inputKey = method.__qualname__ + ":inputs"
    outputKey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        self._redis.rpush(inputKey, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputKey, str(result))
        return result

    return wrapper


""" 4. Retrieving lists """


def replay(method: Callable) -> None:
    """ Decorator """
    method_name = method.__qualname__
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print(f'{method_name} was called {len(inputs)} times:')

    for inp, oup in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) => \
                {oup.decode('utf-8')}")


class Cache:
    """ Cache class """

    def __init__(self):
        """
        Store an instance of the Redis client as a private variable _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key (e.g. using uuid)
        Store the input data in Redis using a random key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    """ 1. Reading from Redis and recovering original type """

    def get(self, key: str, fn: Optional[Callable] = None
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
