from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.user_router import router as user_router

app = FastAPI(
    title="AgroMonitor API",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(user_router)