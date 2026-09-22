from fastapi import FastAPI

from app.api.user_router import router as user_router
from app.api.field_router import router as field_router

app = FastAPI(
    title="AgroMonitor API",
    version="0.1.0"
)


app.include_router(user_router)
app.include_router(field_router)