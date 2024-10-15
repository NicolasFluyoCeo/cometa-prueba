from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.application.health_checkers.dto import HealthCheckReportDTO
from src.presentation.api.commons.response_model import BaseResponseModel
from src.presentation.api.di.stub import readiness_health_check_executor_stub
from src.presentation.api.resources.health_checkers.response_model import (
    LivezResponseModel,
    ReadyzResponseModel,
)

health_checkers_router = APIRouter(prefix="/healthchecks", tags=["health-checkers"])


@health_checkers_router.get(
    "/livez",
    responses={
        status.HTTP_200_OK: {"model": BaseResponseModel[LivezResponseModel]},
    },
    status_code=status.HTTP_200_OK,
)
async def livez() -> BaseResponseModel[LivezResponseModel]:
    return BaseResponseModel(
        error=False,
        message="Successful call to livez",
        data=LivezResponseModel(),
    )


@health_checkers_router.get(
    "/readyz",
    responses={
        status.HTTP_200_OK: {"model": BaseResponseModel[ReadyzResponseModel]},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": BaseResponseModel[ReadyzResponseModel]
        },
    },
    status_code=status.HTTP_200_OK,
)
async def readyz(
    health_check_report: HealthCheckReportDTO = Depends(
        readiness_health_check_executor_stub
    ),
) -> JSONResponse:
    status_code = status.HTTP_200_OK

    if not health_check_report.healthy:
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    content = BaseResponseModel(
        error=not health_check_report.healthy,
        message="Successful call to readyz",
        data=health_check_report,
    ).dict()
    return JSONResponse(status_code=status_code, content=content)
