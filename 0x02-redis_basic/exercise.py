#!/usr/bin/env python3
"""blueprint for creation object of Cache"""
from uuid import uuid4
from redis import Redis
from typing import Union


class Cache:
    """implement properties and methods of class Cache"""

    def __init__(self):
        """ constructor method"""
        self._redis = Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ gen random key and store data in Redis with key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
