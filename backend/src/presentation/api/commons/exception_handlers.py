from typing import Dict, List

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.presentation.api.commons.response_model import BaseResponseModel


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponseModel[Dict](
            error=True, message="An internal server error occurred.", data={}
        ).dict(),
    )


async def not_found_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=BaseResponseModel[Dict](error=True, message=exc.detail, data={}).dict(),
    )


async def validation_error_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=BaseResponseModel[List](
            error=True, message="Errors ocurred during validation", data=exc.errors()
        ).dict(),
    )
