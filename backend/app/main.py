from fastapi import FastAPI

from app.api.user_router import router as user_router
from app.api.field_router import router as field_router
from app.api.sensor_router import router as sensor_router
from app.api.measurement_router import router as measurement_router
from app.api.alert_router import router as alert_router
from app.logging_config import setup_logging


app = FastAPI(
    title="AgroMonitor API",
    version="0.1.0"
)

setup_logging()

app.include_router(user_router)
app.include_router(field_router)
app.include_router(sensor_router)
app.include_router(measurement_router)
app.include_router(alert_router)