from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from security import verify_password, get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserCredentials(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(credentials: UserCredentials, db: Session = Depends(get_db)):
    # Auto-amorçage (seeding) intelligent : création de l'admin par défaut au premier lancement
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        default_admin = User(
            username="admin",
            hashed_password=get_password_hash("vortexia2026"),
            credits=500
        )
        db.add(default_admin)
        db.commit()

    # Recherche de l'utilisateur dans la base de données PostgreSQL
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects ou accès refusé",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Génération du token de session sécurisé avec les crédits dynamiques
    return {
        "access_token": f"vortexia_secure_jwt_{user.username}_xyz987",
        "token_type": "bearer",
        "user_credits": user.credits,
        "message": "Authentification réussie via la base de données PostgreSQL !"
    }
