from typing import Optional


class BookServiceException(Exception):
    """Base exception for the Book Service"""


class BookNotFoundException(BookServiceException):
    """
    Exception raised when a book with the provided criteria is not found.
    """

    def __init__(
        self,
        search_criteria: Optional[str] = None,
        *args,
    ):
        super().__init__(args)
        self.search_criteria = search_criteria

    def __str__(self) -> str:
        return f"No book found matching the criteria: {self.search_criteria}"


class InvalidSearchCriteriaException(BookServiceException):
    """Exception raised when the search criteria are invalid"""

    def __init__(self, criteria: Optional[str] = None, *args):
        super().__init__(args)
        self.criteria = criteria

    def __str__(self) -> str:
        return f"Invalid search criteria: {self.criteria}"


class GenreNotFoundException(BookServiceException):
    """Exception raised when a specific genre is not found"""

    def __init__(self, genre: Optional[str] = None, *args):
        super().__init__(args)
        self.genre = genre

    def __str__(self) -> str:
        return f"Genre not found: {self.genre}"


class ExternalAPIException(BookServiceException):
    """Exception raised when there's an error with the external API"""

    def __init__(
        self,
        api_name: Optional[str] = None,
        error_message: Optional[str] = None,
        *args,
    ):
        super().__init__(args)
        self.api_name = api_name
        self.error_message = error_message

    def __str__(self) -> str:
        return f"Error in external API {self.api_name}: {self.error_message}"
