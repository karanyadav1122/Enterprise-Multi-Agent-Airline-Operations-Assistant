from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.flight_agent import flight_agent
from app.agents.policy_agent import policy_agent
from app.tools.flight_tool import get_flight_status

from app.agents.weather_agent import weather_agent

class AirlineState(TypedDict):
  user_query: str
  intent: str
  response: str
  
def classify_intent(state: AirlineState) :
    query = state['user_query'].lower()
    
    if 'flight' in query or 'aa' in query or 'status' in query or 'delayed' in query:
      intent = "flight"
      
    elif 'baggage' in query or 'policy' in query or 'rebook' in query or 'connection' in query:
      intent = "policy"
      
   
      
    elif "weather" in query :
      intent = "weather"
      
    else:
      intent = "general"
      
    return {"intent": intent} 
  
def route_request(state: AirlineState):
    intent = state['intent']
    query = state['user_query']
    
    if intent == "flight":
      flight_data = get_flight_status("AA123")
      
      response = (
            f"Flight AA123 status: {flight_data['status']}. "
            f"Gate: {flight_data.get('gate', 'N/A')}. "
            f"Departure: {flight_data.get('departure', 'N/A')}. "
            f"Arrival: {flight_data.get('arrival', 'N/A')}."
        )
    
    elif intent ==  "weather":
      response =  weather_agent(state['user_query'])
      
    elif intent == "policy":
      response = policy_agent(state['user_query'])
      
    else:
      response = (
                  "I can help with flight status, baggae policy, rebooking,"
                  "and weather related airlne operations")
      
    return {"response": response}
  
  
workflow = StateGraph(AirlineState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("route_request", route_request)
workflow.set_entry_point("classify_intent")

workflow.add_edge("classify_intent", "route_request")
workflow.add_edge("route_request", END)


graph = workflow.compile()

def run_airline_agent(user_query: str) -> str:
  result = graph.invoke({
    "user_query": user_query,
    "intent": "",
    "response": ""
  }) 
     
  return result['response']




         
               