from typing import Annotated, Dict, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
import json

from src.books.app.exceptions import (
    BookNotFoundException,
    ExternalAPIException,
    GenreNotFoundException,
    InvalidSearchCriteriaException,
)
from src.books.domain.schemas import (
    BookGenreSchema,
    BookListSchema,
    BooksSearchCriteriaSchema,
)
from src.books.domain.searcher.protocols import BookSearcherProtocol
from src.core.domain.broker.broker import BrokerProtocol
from src.core.domain.broker.schemas import MessageSchema
from src.presentation.api.commons.response_model import BaseResponseModel
from src.presentation.api.di.stub import get_books_service_stub, get_broker_stub, get_redis_stub
from src.core.domain.database.schemas import RedisProtocol

logger = structlog.get_logger(module="api", process="books")

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": BaseResponseModel[BookListSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": BaseResponseModel[Dict]},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseModel[Dict]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseResponseModel[Dict]},
    },
)
async def get_books(
    filter_query: Annotated[BooksSearchCriteriaSchema, Query()],
    books_service: BookSearcherProtocol = Depends(get_books_service_stub),
    redis_service: RedisProtocol = Depends(get_redis_stub),
):
    try:
        # Intentamos obtener los libros desde Redis
        books_json = await redis_service.get(filter_query.list)
        if books_json:
            # Deserializamos la cadena JSON a un objeto Python
            books = json.loads(books_json)
            message = "Libros encontrados en caché"
        else:
            # Si no están en Redis, los buscamos en el servicio
            books = await books_service.search_books(filter_query)
            # Almacenamos los libros en Redis para futuras consultas
            await redis_service.set(filter_query.list, books.model_dump_json())
            message = "Libros encontrados satisfactoriamente"

        return BaseResponseModel(
            error=False, message=message, data=books
        )

    except BookNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except InvalidSearchCriteriaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except ExternalAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@books_router.get(
    "/genres",
    responses={
        status.HTTP_200_OK: {"model": BaseResponseModel[List[BookGenreSchema]]},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseModel[Dict]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseResponseModel[Dict]},
    },
)
async def list_genres(
    books_service: BookSearcherProtocol = Depends(get_books_service_stub),
):
    try:
        genres = await books_service.list_genres()
        return BaseResponseModel(
            error=False, message="Genres listed successfully", data=genres
        )
    except GenreNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ExternalAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@books_router.get("/fill")
async def fill_books(
    broker: BrokerProtocol = Depends(get_broker_stub),
    books_service: BookSearcherProtocol = Depends(get_books_service_stub),
):
    genres = await books_service.list_genres()
    for genre in genres:
        logger.info(f"Género: {genre}")
        criteria = BooksSearchCriteriaSchema(list=genre["code"])
        message = MessageSchema(
            payload={"criteria": criteria},
            queue_name=broker.books_queue.name,
        )

        try:
            await broker.publish(message, broker.books_queue.name)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        
    return {"message": "Books filled successfully"}
