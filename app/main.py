from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.observability import tracing
from app.api.chat import router as chat_router
from app.api.health import router as health_router


app = FastAPI(
    title="Enterprise Multi-Agent Airline Operations Assistant",
    version="1.0.0",
)

FastAPIInstrumentor.instrument_app(app)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])