from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["Users & Credits"])

@router.get("/me/credits")
def get_user_credits(username: str, db: Session = Depends(get_db)):
    # Récupération des informations et des crédits de l'utilisateur
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return {
        "username": user.username,
        "credits": user.credits,
        "is_active": user.is_active,
        "created_at": user.created_at
    }
