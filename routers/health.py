from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/health",
    tags=["Monitoring"]
)

@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "Vortexia AI API",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "production"
    }
  
