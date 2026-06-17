from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.health import router as health_router

app = FastAPI(
  title= "Enterprise Mutli-Agent Airline Operations Assitant",
  version = "1.0.0"
)

app.include_router(health_router, prefix = "/health", tags = ['health'])
app.include_router(chat_router, prefix= '/chat', tags = ['chat'])