import asyncio
import signal

import structlog

from src.core.infra.broker.rabbitmq.settings import Settings as RabbitMQSettings
from src.presentation.consumer.settings import Settings as ConsumerSettings

from src.presentation.consumer.broker import get_broker
from src.presentation.consumer.di import setup_di
from src.presentation.consumer.handlers.books import handlers

logger = structlog.get_logger(module="consumer", process="main")


async def init_consumer() -> None:
    logger.info("Iniciando el consumidor...")
    rabbitmq_settings = RabbitMQSettings()
    consumer_settings = ConsumerSettings()

    setup_di()
    logger.info("DI configurado")

    broker =  get_broker(
        consumer_settings=consumer_settings,
        rabbitmq_settings=rabbitmq_settings,
    )
    logger.info("Broker configurado")
    logger.info(f"Broker: {broker.books_queue.name}")

    # Asegurarse de que los manejadores estén registrados
    handlers.broker = broker

    stop_event = asyncio.Event()

    # Configurar manejadores de señales
    signals = (
        signal.SIGHUP,
        signal.SIGTERM,
        signal.SIGINT,
    )

    loop = asyncio.get_running_loop()

    def signal_handler():
        stop_event.set()

    for s in signals:
        loop.add_signal_handler(s, signal_handler)

    # Ejecutar el broker y esperar a la señal de parada
    await asyncio.gather(
        broker.run(),
        stop_event.wait(),
    )

    # Cerrar el broker
    await broker.close()


if __name__ == "__main__":
    asyncio.run(init_consumer())
