import asyncio
import json

import structlog
from fast_depends import Depends, inject
from faststream.exceptions import AckMessage
from faststream.rabbit import RabbitMessage

from src.books.domain.schemas import BooksSearchCriteriaSchema
from src.books.domain.searcher.protocols import BookSearcherProtocol
from src.core.domain.database.schemas import RedisProtocol
from src.core.infra.broker.rabbitmq.settings import Settings as RabbitMQSettings
from src.presentation.consumer.broker import get_broker
from src.presentation.consumer.di.stub import get_books_service_stub, get_redis_stub
from src.presentation.consumer.settings import Settings as ConsumerSettings
import random


class DelayRetryMiddleware:
    ATTEMPT_HEADER = "x-retry-attempt"

    def __init__(self, max_retries: int, delay_ms: int):
        self.max_retries = max_retries
        self.delay_ms = delay_ms

    async def __call__(self, handler, message: RabbitMessage):
        attempt = self._get_attempt_from_message(message)

        while attempt < self.max_retries:
            try:
                # Actualiza el encabezado con el número de intento actual
                message.headers[self.ATTEMPT_HEADER] = attempt
                await handler(message)
                logger.info(
                    f"Mensaje procesado exitosamente en el intento {attempt + 1}"
                )
                return
            except Exception as e:
                attempt += 1
                logger.error(
                    f"Error procesando el mensaje en el intento {attempt}: {e}"
                )
                if attempt >= self.max_retries:
                    logger.error(
                        "Se alcanzó el número máximo de reintentos, enviando a la DLQ"
                    )
                    raise e  # Lanza la excepción después de alcanzar el límite de reintentos
                await asyncio.sleep(
                    self.delay_ms / 1000
                )  # Convierte milisegundos a segundos
                logger.info(
                    f"Reintentando en {self.delay_ms} ms... (Intento {attempt})"
                )

        # Si todos los reintentos fallan, envía el mensaje a la Dead Letter Queue (DLQ)
        logger.error("No se pudo procesar el mensaje, enviando a la DLQ")
        raise AckMessage  # Forzar el acknowledgment para que el mensaje se mueva a la DLQ

    def _get_attempt_from_message(self, message: RabbitMessage) -> int:
        """Obtiene el número de intento desde los headers del mensaje"""
        if self.ATTEMPT_HEADER in message.headers:
            attempt = message.headers[self.ATTEMPT_HEADER]
            try:
                return int(attempt)
            except ValueError:
                logger.warning(
                    f"Encabezado de intento no es un número válido: {attempt}"
                )
        return 0  # Si no existe el header o no es válido, empezamos desde el intento 0


logger = structlog.get_logger(
    module="consumerHandlersBooks",
    process="get_books_consumer",
)
consumer_settings = ConsumerSettings()
rabbitmq_settings = RabbitMQSettings()


broker = get_broker(
    consumer_settings=consumer_settings,
    rabbitmq_settings=rabbitmq_settings,
)


# Modifica tus decoradores para usar una función en lugar del broker directamente


@broker.subscriber(
    broker.books_queue.name,
)
@inject(cast=False)
async def get_books_handler(
    message: RabbitMessage,
    books_service: BookSearcherProtocol = Depends(get_books_service_stub),
    redis_service: RedisProtocol = Depends(get_redis_stub),
):
    max_retries = 3
    delay_seconds = 5

    headers = message.headers or {}
    retries = headers.get("retries", 0)
    logger.info(
        f"Procesando mensaje, intento número {retries + 1}",
        message_id=message.message_id,
    )

    try:
        data = json.loads(message.body)
        criteria = BooksSearchCriteriaSchema(**data["payload"]["criteria"])
        result = await books_service.search_books(criteria)
        logger.info(
            "Libro procesado exitosamente",
            result=result.model_dump(),
            message_id=message.message_id,
        )
        await redis_service.set(criteria.list, result.model_dump())
        await message.ack()
    except Exception as e:
        logger.error(
            f"Error al procesar el mensaje: {e}", message_id=message.message_id
        )

        if retries < max_retries:
            new_headers = message.headers.copy()
            new_headers["retries"] = retries + 1

            logger.info(
                f"Programando reintento {retries + 1} con retraso de {delay_seconds} segundos"
            )

            await asyncio.sleep(delay_seconds)

            await message.nack(requeue=False)

            await broker.publish(
                message.body,
                broker.books_queue.name,
                headers=new_headers,
            )
            logger.info(
                "Mensaje republicado para reintento",
                message_id=message.message_id,
                retry_count=retries + 1,
            )
        else:
            logger.warning(
                f"Mensaje {message.message_id} agotó los reintentos. Enviando a DLQ."
            )
            await broker.publish(message.body, broker.dlq_queue.name)
            await message.ack()

        raise AckMessage()


@broker.subscriber(broker.dlq_queue.name)
@inject(cast=False)
async def dead_letter_handler(
    message: RabbitMessage,
    books_service: BookSearcherProtocol = Depends(get_books_service_stub),
    redis_service: RedisProtocol = Depends(get_redis_stub),
):
    random_number = random.randint(10, 30)
    logger.error(f"Mensaje en cola de letras muertas: {message.body}")
    await asyncio.sleep(random_number)
    data = json.loads(message.body)
    criteria = BooksSearchCriteriaSchema(**data["payload"]["criteria"])
    result = await books_service.search_books(criteria)
    logger.info("libro antes de guardar en redis", result=result.model_dump())
    logger.info("criteria", criteria=criteria)
    await redis_service.set(criteria.list, result.model_dump_json())
    logger.info(
        "Libro procesado exitosamente",
        result=result.model_dump(),
        message_id=message.message_id,
    )
    await message.ack()
