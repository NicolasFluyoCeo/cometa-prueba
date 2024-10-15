from enum import Enum
from functools import lru_cache
from typing import Callable

from src.books.app.service import BooksService
from src.books.infra.searcher.nyt_books.service import NYTBooksClient, NYTBooksService
from src.books.infra.searcher.nyt_books.settings import Settings as NYTBooksSettings
from src.presentation.consumer.settings import Settings as ConsumerSettings
from src.core.infra.database.redis.service import RedisService
from src.core.domain.database.schemas import RedisProtocol
import asyncio

class APISearcherServiceEnum(str, Enum):
    NYT = "nyt"


class SettingsProvider(
    ConsumerSettings,
    NYTBooksSettings,
): ...


class InfrastructureProvider:
    def __init__(
        self,
        get_settings: Callable[[], SettingsProvider],
    ) -> None:
        self._get_settings = get_settings

    def get_books_service(self) -> BooksService:
        if self._get_settings().consumer_book_service == APISearcherServiceEnum.NYT:
            client = NYTBooksClient(
                api_key=self._get_settings().api_key,
                retries=self._get_settings().retries,
                retry_delay=self._get_settings().retry_delay,
                base_url=self._get_settings().base_url,
            )
            return BooksService(NYTBooksService(client=client))
    def get_redis_service(self) -> RedisProtocol:
        redis_service = RedisService()
        asyncio.run(redis_service.setup())
        return redis_service
@lru_cache
def get_settings() -> SettingsProvider:
    return SettingsProvider()
