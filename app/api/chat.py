from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.graph import run_airline_agent
from app.events.kafka_producer import publish_chat_event
from app.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY

import time
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    REQUEST_COUNT.labels(endpoint="/chat", method="POST").inc()

    logger.info(
        f"request_id={request_id} "
        f"user_id={request.user_id} "
        f"event=chat_request_received "
        f"message='{request.message}'"
    )

    result = run_airline_agent(request.message, request.user_id, request_id)

    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/chat").observe(latency)

    latency_ms = latency * 1000

    logger.info(
        f"request_id={request_id} "
        f"user_id={request.user_id} "
        f"event=chat_request_completed "
        f"latency_ms={latency_ms:.2f}"
    )

    publish_chat_event(
        request_id=request_id,
        user_id=request.user_id,
        message=request.message,
        response=result,
    )

    return ChatResponse(response=result)