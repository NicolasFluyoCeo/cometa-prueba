from pydantic import BaseModel

from src.core.application.health_checkers.dto import HealthCheckReportDTO


class LivezResponseModel(BaseModel):
    liveness: bool = True


class ReadyzResponseModel(HealthCheckReportDTO):
    """Response scheme of request to readyz endpoint."""
