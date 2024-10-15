import pytest
from typing import List

from src.books.app.service import BooksService
from src.books.domain.schemas import BookListSchema, BooksSearchCriteriaSchema, BookGenreSchema
from src.books.infra.searcher.dummy.service import DummyBookSearcherService

@pytest.mark.asyncio
class TestBooksService:
    @pytest.fixture
    def dummy_searcher(self):
        return DummyBookSearcherService()

    @pytest.fixture
    def books_service(self, dummy_searcher):
        return BooksService(searcher=dummy_searcher)

    async def test_search_books(self, books_service):
        criteria = BooksSearchCriteriaSchema()
        result = await books_service.search_books(criteria)
        
        assert isinstance(result, BookListSchema)
        assert result.num_results == 1
        assert len(result.results) == 1
        
        book = result.results[0].book_details[0]
        assert book.title == "Libro Dummy"
        assert book.author == "Autor Dummy"

    async def test_list_genres(self, books_service):
        result = await books_service.list_genres()
        
        assert isinstance(result, List)
        assert len(result) == 2
        assert all(isinstance(genre, BookGenreSchema) for genre in result)
        assert result[0].display_name == "Género Dummy 1"
        assert result[1].display_name == "Género Dummy 2"

    async def test_search_books_with_criteria(self, books_service):
        criteria = BooksSearchCriteriaSchema(list="bestsellers", bestsellers_date="2023-05-01")
        result = await books_service.search_books(criteria)
        
        assert isinstance(result, BookListSchema)
        assert result.num_results == 1

    async def test_list_genres_returns_correct_type(self, books_service):
        result = await books_service.list_genres()
        
        assert all(isinstance(genre, BookGenreSchema) for genre in result)

