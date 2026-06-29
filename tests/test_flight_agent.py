from app.agents.flight_agent import flight_agent

def test_flight_agent_status():
  response = flight_agent(
    query= "what is the status of AA123",
    user_id = "test_user",
    request_id= "test_request"
  )
  
  assert "AA123" in response
  assert "ON_TIME" in response
  assert "Gate" in response
  
  
def test_flight_agent_missing_flight_number():
  response =  flight_agent(
    query = "what is my flight status",
    user_id = "new_test_user",
    request_id= "test_request"
  )
  
  assert "Please provide a  valid flight number " in response