from unittest.mock import AsyncMock

import pytest
from src.books.app.exceptions import BookNotFoundException, ExternalAPIException
from src.books.app.use_cases.search_books import SearchBooksUseCase
from src.books.domain.schemas import (
    BookListSchema,
    BookResultSchema,
    BookSchema,
    BooksSearchCriteriaSchema,
    ISBNSchema,
    ReviewSchema,
)


@pytest.fixture
def mock_searcher():
    return AsyncMock()


@pytest.fixture
def search_books_use_case(mock_searcher):
    return SearchBooksUseCase(mock_searcher)


@pytest.mark.asyncio
async def test_search_books_success(search_books_use_case, mock_searcher):
    # Arrange
    criteria = BooksSearchCriteriaSchema(list="Test List")
    expected_books = BookListSchema(
        num_results=1,
        results=[
            BookResultSchema(
                list_name="Test List",
                display_name="Test Display Name",
                bestsellers_date="2023-01-01",
                published_date="2023-01-01",
                rank=1,
                rank_last_week=2,
                weeks_on_list=3,
                asterisk=0,
                dagger=0,
                amazon_product_url="https://example.com",
                isbns=[ISBNSchema(isbn10="1234567890", isbn13="1234567890123")],
                book_details=[
                    BookSchema(
                        title="Test Title",
                        description="Test Description",
                        contributor="Test Contributor",
                        author="Test Author",
                        contributor_note="Test Note",
                        price=19.99,
                        age_group="Adult",
                        publisher="Test Publisher",
                        primary_isbn13="1234567890123",
                        primary_isbn10="1234567890",
                    )
                ],
                reviews=[
                    ReviewSchema(
                        book_review_link="https://example.com/review",
                        first_chapter_link="https://example.com/chapter",
                        sunday_review_link="https://example.com/sunday",
                        article_chapter_link="https://example.com/article",
                    )
                ],
            )
        ],
    )
    mock_searcher.search_books.return_value = expected_books

    # Act
    result = await search_books_use_case(criteria)

    # Assert
    assert result == expected_books
    mock_searcher.search_books.assert_called_once_with(criteria)


@pytest.mark.asyncio
async def test_search_books_no_results(search_books_use_case, mock_searcher):
    # Arrange
    criteria = BooksSearchCriteriaSchema(author="Nonexistent Author")
    mock_searcher.search_books.return_value = None

    # Act & Assert
    with pytest.raises(BookNotFoundException):
        await search_books_use_case(criteria)


@pytest.mark.asyncio
async def test_search_books_external_api_exception(
    search_books_use_case, mock_searcher
):
    # Arrange
    criteria = BooksSearchCriteriaSchema(title="Error Book")
    mock_searcher.search_books.side_effect = Exception("API Error")

    # Act & Assert
    with pytest.raises(ExternalAPIException):
        await search_books_use_case(criteria)


@pytest.mark.asyncio
async def test_search_books_unexpected_exception(search_books_use_case, mock_searcher):
    # Arrange
    criteria = BooksSearchCriteriaSchema(genre="Mystery")
    mock_searcher.search_books.side_effect = ValueError("Unexpected error")

    # Act & Assert
    with pytest.raises(ExternalAPIException):
        await search_books_use_case(criteria)
