from fastapi import FastAPI

app = FastAPI(
    title="Pulse Metrics API",
    description="Plataforma SaaS de Telemetría y Gestión de Operaciones Cloud",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Pulse Metrics API",
        "message": "Bienvenido al núcleo de telemetría. Arquitectura modular activa."
    }