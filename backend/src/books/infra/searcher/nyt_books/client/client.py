import asyncio
from typing import Any, Dict, List, Optional

import httpx
import structlog
from httpx import AsyncClient, HTTPStatusError, Limits, Timeout

from src.books.domain.schemas import BookListSchema

from .exceptions import (
    NYTBooksException,
    NYTBooksInvalidPayloadRequestException,
    NYTBooksTooManyRequestsException,
    NYTBooksUnexpectedStatusResponseException,
)

logger = structlog.get_logger(module="searcher", process="NYTBooksClient")


class Client:
    def __init__(
        self,
        api_key: str,
        retries: int = 3,
        retry_delay: int = 1,
        base_url: str = "https://api.nytimes.com/svc/books/v3",
    ):
        self._api_key = api_key
        self._retries = retries
        self._retry_delay = retry_delay
        self._base_url = base_url
        self._client = AsyncClient(
            base_url=self._base_url,
            timeout=Timeout(10.0),
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )

    async def _do_request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict] = None,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
        file: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> httpx.Response:
        if not params:
            params = {}
        params["api-key"] = self._api_key
        # Filter out None parameters
        params = {k: v for k, v in params.items() if v is not None}
        for attempt in range(self._retries):
            try:
                logger.debug(
                    "Attempting request", method=method, path=path, attempt=attempt + 1
                )
                response = await self._client.request(
                    method=method,
                    url=path,
                    headers=headers,
                    json=json,
                    params=params,
                    files=file,
                    data=data,
                )
                response.raise_for_status()
                return response
            except HTTPStatusError as exc:
                logger.error(
                    "HTTP Error occurred",
                    status_code=exc.response.status_code,
                    method=method,
                    path=path,
                    exc_info=exc,
                )
                if exc.response.status_code == 422:
                    logger.error("Invalid payload request", exc_info=exc)
                    raise NYTBooksInvalidPayloadRequestException(
                        exc.response.json().get("detail", []), exc.response
                    )
                if exc.response.status_code == 429:
                    retry_after = int(
                        exc.response.headers.get("Retry-After", self._retry_delay)
                    )
                    logger.warning(
                        "Too many requests, waiting to retry", retry_after=retry_after
                    )
                    await asyncio.sleep(retry_after)
                    continue
                if attempt == self._retries - 1:
                    logger.error("Unexpected status response", exc_info=exc)
                    raise NYTBooksUnexpectedStatusResponseException(exc.response)
            except Exception as exc:
                logger.error(
                    "Unexpected exception occurred during request",
                    method=method,
                    path=path,
                    exc_info=exc,
                )
                if attempt == self._retries - 1:
                    logger.error(
                        "Maximum retries reached, raising NYTBooksException",
                        exc_info=exc,
                    )
                    raise NYTBooksException(f"Error calling {method} {path}") from exc

            logger.info(
                "Retrying request",
                method=method,
                path=path,
                retry_delay=self._retry_delay,
            )
            await asyncio.sleep(self._retry_delay)
            self._retry_delay *= 2

        logger.error("Maximum number of retries exceeded")
        raise NYTBooksTooManyRequestsException("Maximum number of retries exceeded")

    async def search_books(self, criteria: Dict[str, Any]) -> BookListSchema:
        path = "/lists.json"
        offset = criteria.get("offset", 0)
        # Check if offset is a multiple of 20
        if offset % 20 != 0:
            logger.error("Invalid offset value", offset=offset)
            raise NYTBooksException("Offset must be a multiple of 20")

        params = {
            "list": criteria.get("list", "hardcover-fiction"),
            "bestsellers-date": criteria.get("bestsellers_date"),
            "published-date": criteria.get("published_date"),
            "offset": offset,
        }

        logger.info("Searching for books", criteria=criteria)
        response = await self._do_request("GET", path, params=params)
        data = response.json()
        books = BookListSchema(**data)
        return books

    async def get_books_genres(self) -> List[Dict[str, str]]:
        path = "/lists/names.json"
        response = await self._do_request("GET", path)
        data = response.json()
        return [
            {
                "code": result["list_name_encoded"],
                "display_name": result["display_name"],
            }
            for result in data.get("results", [])
        ]
