#!/usr/bin/env python3
"""This module is a practice exercise on using
Redis
"""


import redis
from typing import Union, Any, Optional, Callable
import uuid


class Cache:
    """This class creates an instnce of the Redis class
    """

    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.

        Args:
        data (Union[str, bytes, int, float]): The data to store.

        Returns:
        str: The key associated with the stored data.
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable[[Any], Any]] = None) -> Any:
        """
        Takes data as input and returns a modified version

        Args:
        key: str: The key associated with the data
        fn: The function that converts the data
        to the desired format

        Returns:
        Any: The data in the modified version
        """

        if key:
            data = self._redis.get(key)
            if data is not None and fn:
                data = fn(data)
            return data
        return None

    def get_str(self, key: str) -> Optional[str]:
        """
        Converts the data back to a string
        """

        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, data: Any) -> int:
        """
        Converts the data back to an integer
        """

        return self.get(key, fn=int)
