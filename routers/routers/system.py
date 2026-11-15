from fastapi import APIRouter

router = APIRouter(
    tags=["System"]
)

@router.get("/")
def read_root():
    return {
        "status": "online",
        "brand": "Vortexia AI",
        "theme": {
            "primary": "Deep Navy (#0B0F19)",
            "accent": "Amber / Copper (#F59E0B)"
        },
        "message": "Vortexia AI Backend is live!"
        }
  
