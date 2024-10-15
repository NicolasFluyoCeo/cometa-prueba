from typing import List, Protocol

from src.books.domain.schemas import (
    BookGenreSchema,
    BookListSchema,
    BooksSearchCriteriaSchema,
)


class BookSearcherProtocol(Protocol):
    """
    Abstract protocol for searching books in an external API.
    """

    async def search_books(self, criteria: BooksSearchCriteriaSchema) -> BookListSchema:
        """
        Search for books based on given criteria.

        Args:
            criteria (BooksSearchCriteriaSchema): An object containing search parameters.

        Returns:
            BookListSchema: A list of books matching the search criteria.
        """

    async def list_genres(self) -> List[BookGenreSchema]:
        """
        Retrieve a list of available book genres.

        Returns:
            List[BookGenreSchema]: A list of book genres.
        """
        ...
