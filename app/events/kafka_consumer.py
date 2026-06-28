import json
import logging

from kafka import KafkaConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
CHAT_EVENTS_TOPIC = "chat-events"


def consume_chat_events() -> None:
    consumer = KafkaConsumer(
        CHAT_EVENTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="chat-events-consumer-group",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    logger.info("Kafka consumer started. Listening for chat events...")

    for message in consumer:
        event = message.value
        logger.info(f"Received chat event: {event}")


if __name__ == "__main__":
    consume_chat_events()