from typing import List

from src.books.domain.schemas import (
    BookGenreSchema,
    BookListSchema,
    BooksSearchCriteriaSchema,
)
from src.books.domain.searcher.protocols import BookSearcherProtocol
from src.books.infra.searcher.nyt_books.client import NYTBooksClient


class NYTBooksService(BookSearcherProtocol):
    def __init__(self, client: NYTBooksClient):
        self._client = client

    async def search_books(self, criteria: BooksSearchCriteriaSchema) -> BookListSchema:
        raw_results = await self._client.search_books(criteria.model_dump())
        return raw_results

    async def get_books_genres(self) -> List[BookGenreSchema]:
        return await self._client.get_books_genres()
