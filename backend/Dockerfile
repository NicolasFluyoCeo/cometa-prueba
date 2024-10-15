FROM python:3.12-slim-bookworm

# Instalar distutils
RUN apt-get update && apt-get install -y python3-distutils

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app
WORKDIR /app

RUN uv sync --frozen
CMD ["uv", "run", "fastapi", "dev", "src/presentation/api/main.py"]