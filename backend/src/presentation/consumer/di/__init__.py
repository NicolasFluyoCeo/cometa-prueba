from fast_depends.dependencies.provider import dependency_provider

from src.presentation.consumer.di.providers import (
    InfrastructureProvider,
    get_settings,
)
from src.presentation.consumer.di.stub import get_books_service_stub, get_redis_stub

infra_provider = InfrastructureProvider(get_settings=get_settings)


def setup_di() -> None:
    dependency_provider.dependency_overrides[
        get_books_service_stub
    ] = infra_provider.get_books_service
    dependency_provider.dependency_overrides[get_redis_stub] = infra_provider.get_redis_service
