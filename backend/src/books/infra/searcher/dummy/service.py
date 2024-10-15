from typing import List

import structlog

from src.books.domain.schemas import (
    BookGenreSchema,
    BookListSchema,
    BookResultSchema,
    BookSchema,
    BooksSearchCriteriaSchema,
    ISBNSchema,
    ReviewSchema,
)
from src.books.domain.searcher.protocols import BookSearcherProtocol

logger = structlog.get_logger(
    module="bookSearcherService", process="DummyBookSearcherService"
)


class DummyBookSearcherService(BookSearcherProtocol):
    async def search_books(self, criteria: BooksSearchCriteriaSchema) -> BookListSchema:
        logger.info(
            f"Buscando libros con criterios: {criteria} en DummyBookSearcherService"
        )

        dummy_book = BookSchema(
            title="Libro Dummy",
            description="Descripción dummy del libro",
            contributor="Contribuidor Dummy",
            author="Autor Dummy",
            price=19.99,
            publisher="Editorial Dummy",
            primary_isbn13="9781234567890",
            primary_isbn10="1234567890",
        )

        dummy_result = BookResultSchema(
            list_name="Lista Dummy",
            display_name="Nombre de Visualización Dummy",
            bestsellers_date="2023-01-01",
            published_date="2023-01-01",
            rank=1,
            rank_last_week=2,
            weeks_on_list=4,
            asterisk=0,
            dagger=0,
            amazon_product_url="https://www.amazon.com/dummy",
            isbns=[ISBNSchema(isbn10="1234567890", isbn13="9781234567890")],
            book_details=[dummy_book],
            reviews=[ReviewSchema()],
        )

        return BookListSchema(num_results=1, results=[dummy_result])

    async def get_books_genres(self) -> List[BookGenreSchema]:
        logger.info("Obteniendo géneros de libros en DummyBookSearcherService")
        return [
            BookGenreSchema(code="DUMMY1", display_name="Género Dummy 1"),
            BookGenreSchema(code="DUMMY2", display_name="Género Dummy 2"),
        ]
