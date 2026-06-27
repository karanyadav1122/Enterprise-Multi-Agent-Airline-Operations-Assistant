import redis

redis_client = redis.Redis(
  host= 'localhost',
  port = 6379,
  db=0,
  decode_responses= True
)

def save_last_flight(user_id: str, flight_number: str) -> None:
  key= f"user:{user_id}:last_flight"
  redis_client.set(key, flight_number)
  
def get_last_flight(user_id: str) -> str | None:
  key = f"user:{user_id}:last_flight"
  return redis_client.get(key)  