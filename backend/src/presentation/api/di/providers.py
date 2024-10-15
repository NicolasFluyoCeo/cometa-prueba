from enum import Enum
from functools import lru_cache
from typing import Callable

from src.books.app.service import BooksService
from src.books.infra.searcher.nyt_books.client import NYTBooksClient
from src.books.infra.searcher.nyt_books.service import NYTBooksService
from src.books.infra.searcher.nyt_books.settings import Settings as NYTBooksSettings
from src.core.application.health_checkers.base import HealthCheckExecutor
from src.core.domain.broker.broker import BrokerProtocol
from src.core.infra.broker.rabbitmq.broker import RabbitMQBroker
from src.core.infra.broker.rabbitmq.settings import Settings as RabbitMQSettings
from src.presentation.api.settings import Settings as APISettings
from src.core.infra.database.redis.service import RedisService
from src.core.domain.database.schemas import RedisProtocol
class APISearcherServiceEnum(str, Enum):
    NYT = "nyt"


class SettingsProvider(
    APISettings,
    NYTBooksSettings,
    RabbitMQSettings,
): ...


@lru_cache
def get_settings() -> SettingsProvider:
    return SettingsProvider()


class InfrastructureProvider:
    def __init__(
        self,
        get_settings: Callable[[], SettingsProvider],
    ) -> None:
        self._get_settings = get_settings

    def get_books_service(self) -> BooksService:
        if self._get_settings().api_searcher_service == APISearcherServiceEnum.NYT:
            client = NYTBooksClient(
                api_key=self._get_settings().api_key,
                retries=self._get_settings().retries,
                retry_delay=self._get_settings().retry_delay,
                base_url=self._get_settings().base_url,
            )
            return BooksService(NYTBooksService(client=client))
        raise ValueError(
            f"Invalid searcher service: {self._get_settings().api_searcher_service}"
        )

    def get_broker(self) -> BrokerProtocol:
        return get_rabbitmq_broker(
            host=self._get_settings().rabbitmq_host,
            port=self._get_settings().rabbitmq_port,
            user=self._get_settings().rabbitmq_user,
            password=self._get_settings().rabbitmq_password,
            vhost=self._get_settings().rabbitmq_vhost,
        )
    
    async def get_redis_service(self) -> RedisProtocol:
        redis_service = RedisService()
        await redis_service.setup()
        return redis_service


@lru_cache
def get_rabbitmq_broker(
    host: str, port: int, user: str, password: str, vhost: str
) -> RabbitMQBroker:
    return RabbitMQBroker(
        settings=RabbitMQSettings(
            rabbitmq_host=host,
            rabbitmq_port=port,
            rabbitmq_user=user,
            rabbitmq_password=password,
            rabbitmq_vhost=vhost,
        )
    )


def readiness_health_check_executor() -> HealthCheckExecutor:
    return HealthCheckExecutor(health_checkers=[])
