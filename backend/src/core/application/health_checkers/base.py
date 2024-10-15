import asyncio
from abc import ABC, abstractmethod
from operator import attrgetter
from typing import List

from src.core.application.health_checkers.dto import (
    CheckResultDTO,
    HealthCheckReportDTO,
)


class Check(ABC):
    @abstractmethod
    async def __call__(self) -> CheckResultDTO:
        raise NotImplementedError()


class HealthCheckExecutor:
    def __init__(self, health_checkers: List[Check]):
        self.__health_checkers = health_checkers

    async def __call__(self) -> HealthCheckReportDTO:
        tasks = [check() for check in self.__health_checkers]
        results = await asyncio.gather(*tasks)

        is_healthy = all(map(attrgetter("passed"), results))

        report = HealthCheckReportDTO(healthy=is_healthy, checks=results)

        return report
