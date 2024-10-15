from fastapi import FastAPI

from src.presentation.api.di.providers import (
    get_settings,
    readiness_health_check_executor,
)
from src.presentation.api.di.stub import (
    get_books_service_stub,
    readiness_health_check_executor_stub,
    get_broker_stub,
    get_redis_stub
)

from .providers import InfrastructureProvider

infra_provider = InfrastructureProvider(get_settings=get_settings)


def setup_di(app: FastAPI) -> None:
    app.dependency_overrides[get_books_service_stub] = infra_provider.get_books_service
    app.dependency_overrides[readiness_health_check_executor_stub] = (
        readiness_health_check_executor
    )
    app.dependency_overrides[get_broker_stub] = infra_provider.get_broker
    app.dependency_overrides[get_redis_stub] = infra_provider.get_redis_service
    app.state.broker = infra_provider.get_broker()
