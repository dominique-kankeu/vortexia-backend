from fastapi import FastAPI
import auth
import users

app = FastAPI(title="Vortexia AI Backend")

# Enregistrement des routeurs
app.include_router(auth.router)
app.include_router(users.router)
