from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.graph import run_airline_agent

router = APIRouter()

class ChatRequest(BaseModel):
  user_id : str
  message: str
  
  
class ChatResponse(BaseModel):
  response : str
  
  
@router.post("", response_model = ChatResponse)
def chat(request: ChatRequest):
  result = run_airline_agent(request.message, request.user_id)
  return ChatResponse(response = result)    