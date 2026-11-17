from fastapi import FastAPI
import routers.auth
import routers.users

app = FastAPI(title="Vortexia AI Backend")

# Enregistrement des routeurs
app.include_router(routers.auth.router)
app.include_router(routers.users.router)
