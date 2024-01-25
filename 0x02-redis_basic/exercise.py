#!/usr/bin/env python3
''' exercise.py '''

import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    decorator that takes a single method argument and returns a Callable
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        increments the count for key every time the method is called
        returns the value returned by the original method
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    '''
    class Cache for redis
    '''
    def __init__(self):
        ''' constructor to create redis instance & flash database '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' method to generate key and store data '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int]:
        ''' converts data back to desired format '''
        data = self._redis.get(key)
        if data is not None:
            if fn is not None:
                return fn(data)
            return data
        return None

    def get_str(self, key: str) -> Optional[str]:
        ''' parametrize Cache.get with the correct str conversion function '''
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        ''' parametrize Cache.get with the correct int conversion function '''
        return self.get(key, fn=int)
