from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
  return{
    "status": "healthy",
    "service": "airline-ops-assistant"
  }