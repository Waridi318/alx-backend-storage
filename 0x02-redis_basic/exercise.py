#!/usr/bin/env python3
"""This module is a practice exercise on using
Redis
"""


import redis
from typing import Union, Any, Optional, Callable
from functools import wraps
import uuid


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        """Defines a wrapper"""
        self = args[0]

        # Generate the Redis keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Convert the arguments to a string and store in Redis using RPUSH
        self._redis.rpush(input_key, str(args))

        # Call the original method and get the result
        result = method(*args, **kwargs)

        # Store the result in Redis using RPUSH
        self._redis.rpush(output_key, str(result))

        # Return the result of the method
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        """Defines a wrapper"""
        # Access the Redis instance via the first argument (self)
        self = args[0]

        # Generate the key based on the method's qualified name
        key = method.__qualname__

        # Increment the count for this key in Redis
        self._redis.incr(key)

        # Call the original method and return its result
        return method(*args, **kwargs)

    return wrapper


class Cache:
    """This class creates an instnce of the Redis class
    """

    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def replay(method: Callable):
        """
        Displays the history of calls of a particular function.

        Args:
        method (Callable): The method to replay the history for.
        """
        # Access the Redis instance via the method's first argument (self)
        self = method.__self__

        # Generate the Redis keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Retrieve the input and output lists from Redis
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)

        # Print the total number of times the method was called
        print(f"{method.__qualname__} was called {len(inputs)} times:")

        """Loop through the inputs and outputs and
        print them in the required format
        """
        for inp, outp in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{inp.decode('utf-8')}) -> "
                  f"{outp.decode('utf-8')}")
