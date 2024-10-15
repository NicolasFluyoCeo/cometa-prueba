from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbitmq_host: str = "backend-rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "pass"
    rabbitmq_vhost: str = "/"
