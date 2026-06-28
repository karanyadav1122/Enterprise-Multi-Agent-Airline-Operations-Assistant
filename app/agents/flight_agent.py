import re
import logging

from app.tools.flight_tool import get_flight_status
from app.cache.redis_client import save_last_flight, get_last_flight, redis_client

logger = logging.getLogger(__name__)


def flight_agent(query: str, user_id: str = "default", request_id: str = "") -> str:
    match = re.search(r"\b[A-Z]{2}\d+\b", query.upper())

    if match:
        flight_number = match.group()
        save_last_flight(user_id, flight_number)
    else:
        flight_number = get_last_flight(user_id)

        if not flight_number:
            return "Please provide a valid flight number like AA456"

    query_lower = query.lower()

    if "gate" in query_lower:
        request_type = "gate"
    elif "departure" in query_lower:
        request_type = "departure"
    elif "arrival" in query_lower:
        request_type = "arrival"
    else:
        request_type = "status"

    cache_key = f"flight_{request_type}:{flight_number}"

    cached_response = redis_client.get(cache_key)

    if cached_response:
        logger.info(
            "request_id=%s user_id=%s flight=%s request_type=%s cache=HIT",
            request_id,
            user_id,
            flight_number,
            request_type,
        )
        return cached_response

    logger.info(
        "request_id=%s user_id=%s flight=%s request_type=%s cache=MISS",
        request_id,
        user_id,
        flight_number,
        request_type,
    )

    flight = get_flight_status(flight_number)

    if flight["status"] == "UNKNOWN":
        return f"Flight {flight_number} not found"

    if request_type == "gate":
        response = f"Flight {flight_number} departs from Gate {flight['gate']}."

    elif request_type == "departure":
        response = f"Flight {flight_number} departs at {flight['departure']}."

    elif request_type == "arrival":
        response = f"Flight {flight_number} arrives at {flight['arrival']}."

    else:
        response = (
            f"Flight {flight_number} status: {flight['status']}. "
            f"Gate: {flight['gate']}. "
            f"Departure: {flight['departure']}. "
            f"Arrival: {flight['arrival']}."
        )

    redis_client.setex(cache_key, 60, response)

    return response