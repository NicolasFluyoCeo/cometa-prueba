from unittest.mock import AsyncMock

import pytest
from src.books.app.exceptions import ExternalAPIException, GenreNotFoundException
from src.books.app.use_cases.list_genres import ListGenresUseCase
from src.books.domain.schemas import BookGenreSchema


@pytest.fixture
def mock_service():
    return AsyncMock()


@pytest.fixture
def list_genres_use_case(mock_service):
    return ListGenresUseCase(mock_service)


@pytest.mark.asyncio
async def test_list_genres_success(list_genres_use_case, mock_service):
    # Arrange
    expected_genres = [
        BookGenreSchema(code="GEN1", display_name="Genre 1"),
        BookGenreSchema(code="GEN2", display_name="Genre 2"),
    ]
    mock_service.get_books_genres.return_value = expected_genres

    # Act
    result = await list_genres_use_case()

    # Assert
    assert result == expected_genres
    mock_service.get_books_genres.assert_called_once()


@pytest.mark.asyncio
async def test_list_genres_empty_result(list_genres_use_case, mock_service):
    # Arrange
    mock_service.get_books_genres.return_value = []

    # Act & Assert
    with pytest.raises(GenreNotFoundException):
        await list_genres_use_case()


@pytest.mark.asyncio
async def test_list_genres_service_exception(list_genres_use_case, mock_service):
    # Arrange
    mock_service.get_books_genres.side_effect = Exception("Service error")

    # Act & Assert
    with pytest.raises(ExternalAPIException):
        await list_genres_use_case()


@pytest.mark.asyncio
async def test_list_genres_unexpected_exception(list_genres_use_case, mock_service):
    # Arrange
    mock_service.get_books_genres.side_effect = ValueError("Unexpected error")

    # Act & Assert
    with pytest.raises(ExternalAPIException):
        await list_genres_use_case()
