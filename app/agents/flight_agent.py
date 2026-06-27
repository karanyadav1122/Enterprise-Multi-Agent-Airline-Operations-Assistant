import re

from app.tools.flight_tool import get_flight_status
from app.cache.redis_client import save_last_flight, get_last_flight

def flight_agent(query: str, user_id: str = 'default') -> str:
  match = re.search(r"\b[A-Z]{2}\d+\b", query.upper())
  
  if match:
    flight_number= match.group()
    save_last_flight(user_id, flight_number)
    
  else:
      flight_number = get_last_flight(user_id)
      
      if not flight_number:
        return "Please provide a valid flight number like AA456"
      
            
  flight = get_flight_status(flight_number)
  
  if flight['status'] == "UNKNOWN":
    return f"Flight {flight_number} not found"
  
  query_lower = query.lower()
  
  if 'gate' in query_lower:
    return f"flight {flight_number} departs from Gate {flight['gate']}."
  
  elif "departure" in query_lower:
    return f"flight {flight_number} departs at {flight['departure']}."
  
  elif 'arrival' in query_lower:
    return f"Flight {flight_number} arrives at {flight['arrival']}"
  
  return (
    f"Flight {flight_number} status: {flight['status']}. "
    f"Gate: {flight['gate']}. "
    f"Departure: {flight['departure']}. "
    f"Arrival: {flight['arrival']}."
)