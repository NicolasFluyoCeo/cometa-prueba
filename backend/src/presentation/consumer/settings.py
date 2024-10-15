from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    consumer_queue: str = "book.queue"
    consumer_book_service: Literal["nyt", "dummy"] = "nyt"
    consumer_max_retries: int = 3
    consumer_ms_delay: int = 1
