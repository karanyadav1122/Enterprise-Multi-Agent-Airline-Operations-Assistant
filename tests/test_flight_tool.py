from app.tools.flight_tool import get_flight_status

def test_known_flight():
  result = get_flight_status("AA456")
  assert result['status'] == "Delayed"
  assert result['gate'] == "B7"
  
def test_unknown_flight():
  result = get_flight_status("AA999")
  assert result['status'] == "UNKNOWN"
  
    