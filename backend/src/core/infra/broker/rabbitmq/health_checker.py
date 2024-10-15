from traceback import format_exc

import aio_pika

from src.core.application.health_checkers.base import Check
from src.core.application.health_checkers.dto import CheckResultDTO


class RabbitMQCheck(Check):
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        port: int = 5672,
        secure: bool = False,
        timeout: float = 60.0,
        name: str = "RabbitMQ",
        vhost: str = "/",
    ):
        self.__host = host
        self.__port = port
        self.__secure = secure
        self.__user = user
        self.__password = password
        self.__timeout = timeout
        self.__name = name
        self.__vhost = vhost

    async def __call__(self) -> CheckResultDTO:
        try:
            async with await aio_pika.connect_robust(
                host=self.__host,
                port=self.__port,
                login=self.__user,
                password=self.__password,
                ssl=self.__secure,
                timeout=self.__timeout,
                virtualhost=self.__vhost,
            ):
                return CheckResultDTO(name=self.__name, passed=True)
        except Exception:
            details = format_exc()
            return CheckResultDTO(name=self.__name, passed=False, details=details)
