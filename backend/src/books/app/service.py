from typing import List

from src.books.app.use_cases.list_genres import ListGenresUseCase
from src.books.app.use_cases.search_books import SearchBooksUseCase
from src.books.domain.schemas import BookListSchema, BooksSearchCriteriaSchema
from src.books.domain.searcher.protocols import BookSearcherProtocol


class BooksService:
    def __init__(self, searcher: BookSearcherProtocol):
        self._searcher = searcher

    async def search_books(self, criteria: BooksSearchCriteriaSchema) -> BookListSchema:
        search_books_use_case = SearchBooksUseCase(self._searcher)
        return await search_books_use_case(criteria)

    async def list_genres(self) -> List[str]:
        list_genres_use_case = ListGenresUseCase(self._searcher)
        return await list_genres_use_case()

