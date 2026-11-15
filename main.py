from fastapi import FastAPI
from routers import system, health

app = FastAPI(
    title="Vortexia AI Backend",
    version="1.0.0",
    description="Backend officiel de Vortexia AI - Architecture Haute Performance"
)

# Inclusion des routeurs modulaires
app.include_router(system.router)
app.include_router(health.router)
