from typing import Protocol, Any


class RedisProtocol(Protocol):
    async def set(self, key: str, value: Any) -> None:
        """
        Set a value for a given key in Redis.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
        """
        ...

    async def get(self, key: str) -> Any:
        """
        Get the value associated with a given key from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Any: The value associated with the key, or None if the key doesn't exist.
        """
        ...
