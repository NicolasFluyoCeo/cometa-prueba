from typing import Dict, List

import httpx


class NYTBooksException(Exception):
    """Base exception for the NYTBooks client"""


class NYTBooksUnexpectedStatusResponseException(NYTBooksException):
    """Exception raised when a response with an unknown status code
    is received in a call to the NYTBooks API"""

    def __init__(self, response: httpx.Response, *args):
        super().__init__(args)
        self.response = response

    def __str__(self) -> str:
        return f"An unexpected status code was received during call to {self.response.request.method} {self.response.request.url}: {self.response.status_code}"


class NYTBooksInvalidPayloadRequestException(NYTBooksException):
    """Exception raised when a status code (422) is received indicating
    that there was a validation error on the data sent."""

    def __init__(self, detail: List[Dict], response: httpx.Response, *args):
        super().__init__(args)
        self.detail = detail
        self.response = response

    def __str__(self) -> str:
        return f"A validation error occurred on the data sent: {self.detail} during call to {self.response.request.method} {self.response.request.url}"


class NYTBooksTooManyRequestsException(NYTBooksException):
    """Exception raised when too many requests are made to the NYTBooks API"""

    def __str__(self) -> str:
        return "Too many requests were made to the NYTBooks API"
