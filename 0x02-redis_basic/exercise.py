#!/usr/bin/env python3
"""blueprint for creation object of Cache"""
import uuid
import redis
from typing import Union
from typing import Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_list = f"{method.__qualname__}:inputs"
        output_list = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_list, str(args))
        method_result = method(self, *args, **kwargs)
        self._redis.rpush(output_list, str(method_result))
        return method_result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """implement properties and methods of class Cache"""

    def __init__(self):
        """ constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def replay(self, method: Callable) -> None:
        """
        display the history of calls of a particular function
        """
        func_name = method.__qualname__
        nb_calls = self.get(func_name).decode('utf-8')
        print(f"{func_name} was called {nb_calls} times:")
        input_key = f"{func_name}:inputs"
        output_key = f"{func_name}:outputs"
        input_list = self._redis.lrange(input_key, 0, -1)
        output_list = self._redis.lrange(output_key, 0, -1)
        for input, output in zip(input_list, output_list):
            print('{}(*{}) -> {}'.format(func_name, input.decode("utf-8"),
                                         output.decode("utf-8"),))
