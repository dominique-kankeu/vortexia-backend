from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["Users"])

class UserRegister(BaseModel):
    phone_number: str
    referral_code: str = None

@router.post("/register")
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    # Vérifier si le numéro de téléphone est déjà enregistré
    existing_user = db.query(User).filter(User.phone_number == data.phone_number).first()
    
    if existing_user:
        return {
            "status": "success",
            "message": "Bon retour sur Vortexia AI !",
            "user_id": existing_user.id,
            "phone_number": existing_user.phone_number,
            "credits": existing_user.credits,
            "referral_code": existing_user.referral_code
        }
    
    # Générer un code de parrainage unique basé sur le numéro (ex: VRT + derniers chiffres ou similaire)
    generated_referral_code = "VRT-" + data.phone_number[-4:]
    
    # Gérer la logique du parrain si un code valide est fourni
    if data.referral_code:
        referrer = db.query(User).filter(User.referral_code == data.referral_code).first()
        if referrer:
            referrer.referral_count += 1
            # Si le parrain atteint 5 filleuls, on lui offre les 100 crédits bonus
            if referrer.referral_count == 5:
                referrer.credits += 100.0

    # Créer le nouveau compte avec 50 crédits de bienvenue
    new_user = User(
        phone_number=data.phone_number,
        credits=50.0,
        referral_code=generated_referral_code,
        referred_by=data.referral_code,
        referral_count=0
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "status": "success",
        "message": "Inscription réussie ! 50 crédits de bienvenue offerts.",
        "user_id": new_user.id,
        "phone_number": new_user.phone_number,
        "credits": new_user.credits,
        "referral_code": new_user.referral_code
    }
