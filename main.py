from fastapi import FastAPI
import routers.system
import routers.users

app = FastAPI(title="Vortexia AI Backend")

# Enregistrement des routeurs
app.include_router(routers.system.router)
app.include_router(routers.users.router)
