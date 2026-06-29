from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response



app = FastAPI(
  title= "Enterprise Mutli-Agent Airline Operations Assitant",
  version = "1.0.0"
)

@app.get("/metrics")
def metrics():
  return Response(generate_latest(), media_type= CONTENT_TYPE_LATEST)



app.include_router(health_router, prefix = "/health", tags = ['health'])
app.include_router(chat_router, prefix= '/chat', tags = ['chat'])