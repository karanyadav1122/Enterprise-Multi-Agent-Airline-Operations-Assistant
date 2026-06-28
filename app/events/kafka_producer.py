import json
import logging
from datetime import datetime, timezone

from kafka import KafkaProducer

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
CHAT_EVENTS_TOPIC = "chat-events"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)


def publish_chat_event(
    request_id: str,
    user_id: str,
    message: str,
    response: str,
) -> None:

    event = {
        "request_id": request_id,
        "user_id": user_id,
        "message": message,
        "response": response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        producer.send(CHAT_EVENTS_TOPIC, event)
        producer.flush()

        logger.info(
            "request_id=%s user_id=%s topic=%s event=kafka_publish_success",
            request_id,
            user_id,
            CHAT_EVENTS_TOPIC,
        )

    except Exception as e:
        logger.error(
            "request_id=%s user_id=%s event=kafka_publish_failed error=%s",
            request_id,
            user_id,
            e,
        )