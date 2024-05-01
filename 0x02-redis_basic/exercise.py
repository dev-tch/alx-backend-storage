#!/usr/bin/env python3
"""blueprint for creation object of Cache"""
import uuid
import redis
from typing import Union
from typing import Callable


class Cache:
    """implement properties and methods of class Cache"""

    def __init__(self):
        """ constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ gen random key and store data in Redis with key"""
        key_value = str(uuid.uuid4())
        self._redis.set(key_value, data)
        return key_value

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """ retrieve redis data after conversion with function fn"""
        redis_data = self._redis.get(key)
        return fn(redis_data) if fn is not None else redis_data

    def get_str(self, key: str) -> Union[str, None]:
        """ get string value from redis database"""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """ get integer value from redis database"""
        return self.get(key, lambda x: int(x))
