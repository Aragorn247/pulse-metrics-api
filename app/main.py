from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(
    title="Pulse Metrics API",
    description="Plataforma SaaS de Telemetría y Gestión de Operaciones Cloud",
    version="1.0.0"
)

# Incluimos las rutas de la API v1 (incluyendo el módulo de autenticación)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Pulse Metrics API",
        "message": "Bienvenido al núcleo de telemetría. Arquitectura modular activa."
    }