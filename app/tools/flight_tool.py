def get_flight_status(flight_number: str) -> dict:
  mock_flights = {
    "AA123": {
      "status": "ON_TIME",
      "gate": "A12",
      "departure": "10.30 AM",
      "arrival": "1.45 PM"
    },
    
    "AA456":{
      "status": "Delayed",
      "gate": "B7",
      "departure": "12.15 PM",
      "arrival" : "3.40 PM"
    }
  }
  
  return mock_flights.get(
    flight_number.upper(),
    {"status":"UNKNOWN","message":"Flight not found"}
  )