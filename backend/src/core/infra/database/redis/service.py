import redis.asyncio as redis
from typing import Any
from src.core.domain.database.schemas import RedisProtocol

class RedisClient:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await redis.from_url("redis://backend-redis:6379")

    async def close(self):
        if self.connection:
            await self.connection.close()

class RedisService(RedisProtocol):
    def __init__(self):
        self.client = RedisClient()

    async def setup(self):
        await self.client.connect()

    async def set(self, key: str, value: Any) -> None:
        await self.client.connection.set(key, value)

    async def get(self, key: str) -> Any:
        return await self.client.connection.get(key)

    async def close(self):
        await self.client.close()
