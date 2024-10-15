from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str = "BGdJALTJJm4HmNPs4PRfzsCKZWKi9Gmq"
    base_url: str = "https://api.nytimes.com/svc/books/v3"
    retries: int = 3
    retry_delay: int = 3

    class Config:
        env_prefix = "NYT_"
        case_sensitive = False
