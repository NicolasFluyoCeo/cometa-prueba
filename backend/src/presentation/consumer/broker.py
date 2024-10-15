import structlog

from src.core.infra.broker.rabbitmq.broker import RabbitMQBroker
from src.core.infra.broker.rabbitmq.settings import Settings as RabbitMQSettings
from src.presentation.consumer.settings import Settings as ConsumerSettings

logger = structlog.get_logger(module="consumerBroker", process="broker")




def get_broker(
    rabbitmq_settings: RabbitMQSettings, consumer_settings: ConsumerSettings
) -> RabbitMQBroker:
    broker = RabbitMQBroker(
        settings=RabbitMQSettings(
            rabbitmq_host=rabbitmq_settings.rabbitmq_host,
            rabbitmq_port=rabbitmq_settings.rabbitmq_port,
            rabbitmq_user=rabbitmq_settings.rabbitmq_user,
            rabbitmq_password=rabbitmq_settings.rabbitmq_password,
            rabbitmq_vhost=rabbitmq_settings.rabbitmq_vhost,
        )
    )

    return broker
