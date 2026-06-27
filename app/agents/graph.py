from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.flight_agent import flight_agent
from app.agents.policy_agent import policy_agent
from app.agents.intent_classifier import classify_user_intent
from app.observability.logger import logger


from app.agents.weather_agent import weather_agent

class AirlineState(TypedDict):
  user_query: str
  intent: str
  response: str
  user_id: str
  
def classify_intent(state: AirlineState):
  intent = classify_user_intent(state['user_query'])
  return {"intent": intent}
  
def route_request(state: AirlineState):
    intent = state["intent"]
    query = state["user_query"]
    user_id = state['user_id']
    logger.info(f"user_id={user_id} intent={intent} query={query}")
    logger.debug(f"DEBUG LOG: user_id={user_id} intent={intent}")

    if intent == "flight":
        response = flight_agent(query,user_id)

    elif intent == "weather":
        response = weather_agent(query)

    elif intent == "policy":
        response = policy_agent(query)

    else:
        response = (
            "I can help with flight status, baggage policy, "
            "rebooking, and weather related airline operations."
        )

    return {"response": response}
  
  
workflow = StateGraph(AirlineState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("route_request", route_request)
workflow.set_entry_point("classify_intent")

workflow.add_edge("classify_intent", "route_request")
workflow.add_edge("route_request", END)
 

graph = workflow.compile()

def run_airline_agent(user_query: str, user_id: str) -> str:
  result = graph.invoke({
    "user_query": user_query,
    "user_id": user_id,
    "intent": "",
    "response": ""
  }) 
     
  return result['response']




         
               