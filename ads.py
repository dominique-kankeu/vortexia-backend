from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/ads", tags=["Ads"])

class AdReward(BaseModel):
    phone_number: str

@router.post("/reward")
def claim_ad_reward(data: AdReward, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == data.phone_number).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    # Ajouter 5 crédits après le visionnage d'une publicité
    reward_amount = 5.0
    user.credits += reward_amount
    db.commit()

    return {
        "status": "success",
        "message": f"+{reward_amount} crédits ajoutés avec succès !",
        "new_balance": user.credits
    }
