from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_searcher_service: Literal["nyt"] = "nyt"
