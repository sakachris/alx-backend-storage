#!/usr/bin/env python3
''' exercise.py '''

import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    The count is stored in Redis using the method's qualified name as the key.
    """
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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Inputs are stored in a Redis list at <method_name>:inputs.
    Outputs are stored in a Redis list at <method_name>:outputs.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store input arguments and output in Redis lists."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper

def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method whose history to display.
    """
    redis_client = method.__self__._redis
    qualname = method.__qualname__
    input_key = f"{qualname}:inputs"
    output_key = f"{qualname}:outputs"

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    print(f"{qualname} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{qualname}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")


# def replay(method: Callable) -> None:
#     """
#     Display the history of calls of a particular function.

#     Args:
#         method (Callable): The method whose history to display.
#     """
#     redis_client = method.__self__._redis
#     qualname = method.__qualname__
#     input_key = f"{qualname}:inputs"
#     output_key = f"{qualname}:outputs"

#     inputs = redis_client.lrange(input_key, 0, -1)
#     outputs = redis_client.lrange(output_key, 0, -1)

#     print(f"{qualname} was called {len(inputs)} times:")
#     for input_data, output_data in zip(inputs, outputs):
#         print(
#             f"{qualname}(*{
#                 input_data.decode('utf-8')
#             }) -> {output_data.decode('utf-8')}"
#         )


class Cache:
    '''
    class Cache for redis
    '''
    def __init__(self) -> None:
        """Initialize the Cache instance and flush existing Redis data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    # def get(
    #         self, key: str, fn: Optional[Callable] = None
    # ) -> Union[str, bytes, int]:
    #     ''' converts data back to desired format '''
    #     data = self._redis.get(key)
    #     if data is not None:
    #         if fn is not None:
    #             return fn(data)
    #         return data
    #     return None

    # def get_str(self, key: str) -> Optional[str]:
    #     ''' parametrize Cache.get with correct str conversion function '''
    #     return self.get(key, fn=lambda d: d.decode("utf-8"))

    # def get_int(self, key: str) -> Optional[int]:
    #     ''' parametrize Cache.get with correct int conversion function '''
    #     return self.get(key, fn=int)

    def get(
            self, key: str, fn: Optional[Callable] = None
    ) -> Union[bytes, str, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The Redis key.
            fn (Callable, optional): Function to convert the data.

        Returns:
            The retrieved and optionally converted data.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a UTF-8 string from Redis by decoding the stored bytes.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[str]: The decoded string or None if key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis by converting the stored bytes.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[int]: The integer value or None if key does not exist.
        """
        return self.get(key, fn=int)
