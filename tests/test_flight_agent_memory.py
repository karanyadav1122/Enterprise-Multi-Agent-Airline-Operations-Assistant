from app.agents.flight_agent import flight_agent
from app.cache.redis_client import redis_client

def test_flight_agent_remembers_last_flight():
  redis_client.delete("user:test_user:last_flight")
  
  response1 = flight_agent("What is the status of AA456?", "test_user")
  response2 = flight_agent("What gate?", "test_user")
  
  assert "AA456" in response1
  assert "Gate B7" in response2
  
  
def test_flight_agent_requires_flight_for_new_user():
  redis_client.delete("user:new_test_user:last_flight")
  
  response = flight_agent("what gate?","new_test_user")
  
  assert "Please provide a valid flight number" in response   
  