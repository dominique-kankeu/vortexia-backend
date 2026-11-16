from fastapi import FastAPI
from routers import auth, users  # <-- Importe le routeur users

app = FastAPI(title="Vortexia AI Backend")

# Enregistrement des routeurs
app.include_router(auth.router)
app.include_router(users.router)  # <-- Ajoute cette ligne si ce n'est pas déjà fait
