from typing import List

from src.books.app import exceptions
from src.books.domain.searcher.protocols import BookSearcherProtocol
import structlog
logger = structlog.get_logger(module="searcher", process="ListGenresUseCase")


class ListGenresUseCase:
    def __init__(self, service: BookSearcherProtocol):
        self._service = service

    async def __call__(self) -> List[str]:
        try:
            genres = await self._service.get_books_genres()
            if not genres:
                logger.error("No genres found")
                raise exceptions.GenreNotFoundException()
            return genres
        except exceptions.BookServiceException as e:
            logger.error("BookServiceException occurred", error=str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error occurred", error=str(e))
            raise exceptions.ExternalAPIException("NYT Books API", str(e))
