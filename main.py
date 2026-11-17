from fastapi import FastAPI
from database import engine
import models
import routers.system
import routers.users
import routers.ads  # <-- 1. Importe le routeur de publicités

# Crée les tables dans la base de données au démarrage
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vortexia AI Backend")

app.include_router(routers.system.router)
app.include_router(routers.users.router)
app.include_router(routers.ads.router)  # <-- 2. Enregistre le routeur
