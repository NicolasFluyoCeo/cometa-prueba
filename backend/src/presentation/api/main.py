from contextlib import asynccontextmanager
from typing import Dict, List

import structlog
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.core.infra.logger.setup import setup_logger
from src.presentation.api.commons.exception_handlers import (
    generic_exception_handler,
    not_found_exception_handler,
    validation_error_exception_handler,
)
from src.presentation.api.commons.response_model import BaseResponseModel
from src.presentation.api.di import setup_di
from src.presentation.api.resources.books.routes import books_router
from src.presentation.api.resources.health_checkers.routes import health_checkers_router

common_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseResponseModel[Dict]},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": BaseResponseModel[List]},
}
docs_url = "/docs"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configuración que se ejecuta al inicio
    setup_logger()
    logger = structlog.get_logger(module="global", process="bootstrapAPI")
    logger.info("Initializing API")
    
    # Conectar el broker
    broker = app.state.broker
    await broker.connect()
    logger.info("RabbitMQ broker connected")
    
    yield
    
    # Limpieza al cierre
    await broker.close()
    logger.info("RabbitMQ broker disconnected")

def create_application() -> FastAPI:
    app = FastAPI(
        openapi_url=f"{docs_url}/openapi.json",
        docs_url=docs_url,
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    common_router_args = {
        "responses": common_responses,
    }
    
    app.include_router(health_checkers_router, **common_router_args)
    app.include_router(books_router)
    
    app.add_exception_handler(Exception, handler=generic_exception_handler)
    app.add_exception_handler(status.HTTP_404_NOT_FOUND, handler=not_found_exception_handler)
    app.add_exception_handler(RequestValidationError, handler=validation_error_exception_handler)
    
    setup_di(app=app)

    return app

api = create_application()
