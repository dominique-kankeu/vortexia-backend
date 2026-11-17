from fastapi import FastAPI
from routers import auth
from routers import users

app = FastAPI(title="Vortexia AI Backend")

# Enregistrement des routeurs
app.include_router(auth.router)
app.include_router(users.router)
