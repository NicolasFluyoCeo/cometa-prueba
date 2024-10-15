from typing import Callable

import structlog
from aio_pika import IncomingMessage

logger = structlog.get_logger(module="rabbitMQBroker", process="exceptionHandling")


def process_message_exception_handler(process_message: Callable) -> Callable:
    async def wrapper(self, message: IncomingMessage, *args, **kwargs):
        try:
            await process_message(self, message, *args, **kwargs)
        except Exception as exc:
            logger.error(f"Rejecting message due to: {str(exc)}", exc_info=exc)
            await message.reject()
        else:
            await message.ack()

    return wrapper
