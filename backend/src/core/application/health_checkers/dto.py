from typing import List, Optional

from pydantic import BaseModel


class CheckResultDTO(BaseModel):
    name: str
    passed: bool
    details: Optional[str] = None


class HealthCheckReportDTO(BaseModel):
    healthy: bool
    checks: List[CheckResultDTO]
