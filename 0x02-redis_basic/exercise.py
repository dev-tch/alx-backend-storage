#!/usr/bin/env python3
"""blueprint for creation object of Cache"""
import uuid
import redis
from typing import Union


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
