from src.books.domain.schemas import BookListSchema, BooksSearchCriteriaSchema
from src.books.domain.searcher.protocols import BookSearcherProtocol
from src.books.app import exceptions
import structlog

logger = structlog.get_logger(module="searcher", process="SearchBooksUseCase")
    

class SearchBooksUseCase:
    def __init__(self, searcher: BookSearcherProtocol):
        self._searcher = searcher

    async def __call__(self, criteria: BooksSearchCriteriaSchema) -> BookListSchema:
        try:
            books = await self._searcher.search_books(criteria)
            if not books:
                logger.error("No books found matching criteria", criteria=str(criteria))
                raise exceptions.BookNotFoundException(str(criteria))
            return books
        except exceptions.BookServiceException as e:
            logger.error("BookServiceException occurred", error=str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error occurred", error=str(e))
            raise exceptions.ExternalAPIException("NYT Books API", str(e))
