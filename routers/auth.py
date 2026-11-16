from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class UserCredentials(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(credentials: UserCredentials):
    if credentials.username == "admin" and credentials.password == "vortexia2026":
        return {
            "access_token": "vortexia_secure_jwt_token_sample_xyz987",
            "token_type": "bearer",
            "message": "Authentification réussie !"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants incorrects"
    )
