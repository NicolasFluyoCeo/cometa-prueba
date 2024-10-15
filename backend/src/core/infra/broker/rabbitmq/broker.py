from typing import Callable, List, Optional

import structlog
from faststream import FastStream
from faststream.rabbit import (
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
)
from faststream import BaseMiddleware
from src.core.domain.broker.schemas import MessageSchema
from src.core.infra.broker.rabbitmq.settings import Settings

logger = structlog.get_logger(module="rabbitMQBroker", process="rabbitMQIntegration")


class RabbitMQBroker:
    """
    A singleton class for managing RabbitMQ connections and operations.

    This class uses the FastStream library to handle RabbitMQ interactions.
    It provides methods for connecting, publishing messages, and subscribing to queues.

    Attributes:
        _instance: Class attribute to store the single instance.
        settings (Settings): Configuration settings for RabbitMQ.
        __handler (Optional[Callable]): Handler for message processing.
        __max_retries (Optional[int]): Maximum number of retry attempts.
        __ms_delay (Optional[int]): Delay between retry attempts in milliseconds.
        __broker (RabbitBroker): FastStream RabbitBroker instance.
        app (FastStream): FastStream application instance.
        __connected (bool): Flag indicating connection status.
        books_exchange (RabbitExchange): Exchange for book-related messages.
        books_queue (RabbitQueue): Queue for book-related messages.
        dlq_queue (RabbitQueue): Dead letter queue for unprocessed messages.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RabbitMQBroker, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.settings = settings
        self.__handler: Optional[Callable] = None
        self.__max_retries: Optional[int] = None
        self.__ms_delay: Optional[int] = None

        self.__broker = RabbitBroker(
            url=f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:{settings.rabbitmq_port}/{settings.rabbitmq_vhost}"
        )
        self.app = FastStream(self.__broker)
        self.__connected = False

        self.books_exchange = RabbitExchange("books_exchange")
        self.books_queue = RabbitQueue("book.queue")
        self.dlq_queue = RabbitQueue("book.queue.dlq")

    async def connect(self) -> None:
        """
        Establishes a connection to RabbitMQ and sets up exchanges and queues.

        This method connects to RabbitMQ using the FastStream broker and calls
        the __setup_rabbitmq method to declare exchanges and queues.
        """
        if not self.__connected:
            await self.__broker.connect()
            await self.__setup_rabbitmq()
            self.__connected = True
            logger.info("RabbitMQ broker connected and setup completed")

    async def __setup_rabbitmq(self) -> None:
        """
        Sets up RabbitMQ exchanges and queues.

        This method declares the necessary exchanges and queues, and binds
        them as required for the application's messaging needs.
        """
        await self.__broker.declare_exchange(self.books_exchange)

        books_queue = await self.__broker.declare_queue(self.books_queue)
        await self.__broker.declare_queue(self.dlq_queue)

        await books_queue.bind(
            self.books_exchange.name, routing_key=self.books_queue.name
        )

        logger.info("RabbitMQ exchanges and queues setup completed")

    async def publish(self, message: MessageSchema, queue_name: str, headers: Optional[dict] = None) -> None:
        """
        Publishes a message to the specified queue.

        Args:
            message (MessageSchema): The message to be published.
            queue_name (str): The name of the queue to publish to.
        """
        logger.info(f"Publicando mensaje en la cola {queue_name}")
        try:
            if not self.__connected:
                await self.connect()
            await self.__broker.publish(message, queue_name, headers=headers)
        except Exception as e:
            logger.error(f"Error al publicar en la cola {queue_name}: {e}")

    async def run(self) -> None:
        """
        Runs the FastStream application asynchronously.

        This method connects to RabbitMQ and starts the FastStream application.
        """
        await self.connect()
        await self.app.run()

    async def close(self) -> None:
        """
        Closes the RabbitMQ connections.

        This method stops the FastStream application and marks the connection as closed.
        """
        logger.info("Cerrando conexiones RabbitMQ")
        await self.app.stop()
        self.__connected = False

    def subscriber(
        self,
        queue: RabbitQueue,
        exchange: Optional[RabbitExchange] = None,
        middlewares: Optional[List[BaseMiddleware]] = None,
    ):
        """
        Decorator for subscribing to a queue.

        Args:
            queue (RabbitQueue): The queue to subscribe to.
            exchange (Optional[RabbitExchange]): The exchange to use, if any.

        Returns:
            A decorator function for subscribing to the specified queue.
        """
        if exchange:
            return self.__broker.subscriber(queue, exchange, middlewares=middlewares)
        return self.__broker.subscriber(queue)
