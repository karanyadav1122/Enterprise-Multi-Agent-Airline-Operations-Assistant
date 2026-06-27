import redis
from app.core.config import settings

redis_client = redis.Redis(
  host= settings.redis_host,
  port = settings.redis_port,
  db=settings.redis_db,
  decode_responses= True
)

def save_last_flight(user_id: str, flight_number: str) -> None:
  key= f"user:{user_id}:last_flight"
  redis_client.set(key, flight_number)
  
def get_last_flight(user_id: str) -> str | None:
  key = f"user:{user_id}:last_flight"
  return redis_client.get(key)  