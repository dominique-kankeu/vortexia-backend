import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Récupération de l'URL de la base de données depuis les variables d'environnement Render, 
# avec un fallback en local si besoin (SQLite pour les tests)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vortexia.db")

# Ajustement pour PostgreSQL sur Render si l'URL commence par postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Fonction utilitaire pour obtenir la session de base de données dans les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
