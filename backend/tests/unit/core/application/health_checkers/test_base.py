import unittest

from src.core.application.health_checkers.base import Check, HealthCheckExecutor
from src.core.application.health_checkers.dto import CheckResultDTO


class ConcreteCheck(Check):
    def __init__(self, name: str, passed: bool):
        super().__init__()
        self.name = name
        self.passed = passed

    async def __call__(self) -> CheckResultDTO:
        return CheckResultDTO(name=self.name, passed=self.passed)


class TestHealthCheckExecutor(unittest.IsolatedAsyncioTestCase):
    async def test_multiple_checkers_passed(self):
        checker1 = ConcreteCheck(name="checker1", passed=True)
        checker2 = ConcreteCheck(name="checker2", passed=True)

        health_check_executor = HealthCheckExecutor([checker1, checker2])

        health_check_report = await health_check_executor()

        assert health_check_report.healthy
        assert len(health_check_report.checks) == 2

    async def test_multiple_checkers_one_fails(self):
        checker1 = ConcreteCheck(name="checker1", passed=False)
        checker2 = ConcreteCheck(name="checker2", passed=True)

        health_check_executor = HealthCheckExecutor([checker1, checker2])

        health_check_report = await health_check_executor()

        assert not health_check_report.healthy
        assert len(health_check_report.checks) == 2

    async def test_multiple_checkers_all_fail(self):
        checker1 = ConcreteCheck(name="checker1", passed=False)
        checker2 = ConcreteCheck(name="checker2", passed=False)

        health_check_executor = HealthCheckExecutor([checker1, checker2])

        health_check_report = await health_check_executor()

        assert not health_check_report.healthy
        assert len(health_check_report.checks) == 2
