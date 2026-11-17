from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    credits = Column(Float, default=50.0) # 50 crédits de bienvenue offerts
    referral_code = Column(String, unique=True, index=True, nullable=True) # Code unique de l'utilisateur
    referred_by = Column(String, nullable=True) # Code de parrain utilisé lors de l'inscription
    referral_count = Column(Integer, default=0) # Nombre de filleuls actifs
    created_at = Column(DateTime, default=datetime.utcnow)
