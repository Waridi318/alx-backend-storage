#!/usr/bin/env python3
"""This module is a practice exercise on using
Redis
"""


import redis
from typing import Union
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
