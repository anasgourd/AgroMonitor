from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.user_router import router as user_router
from app.api.field_router import router as field_router
from app.api.sensor_router import router as sensor_router
from app.api.measurement_router import router as measurement_router
from app.api.alert_router import router as alert_router
from app.api.metrics_router import router as metrics_router
from app.logging_config import setup_logging
from app.core.database import SessionLocal
from app.mqtt.consumer import MQTTConsumer


# Manages the application's startup and shutdown lifecycle.
# Starts the MQTT consumer when FastAPI starts and stops it on shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):

    consumer = MQTTConsumer(
        broker="localhost",
        port=1883,
        session_factory=SessionLocal
    )

    consumer.start()

    try:
        yield
    finally:
        consumer.stop()
        
app = FastAPI(
    title="AgroMonitor API",
    version="0.1.0",
    lifespan=lifespan
)

setup_logging()

app.include_router(user_router)
app.include_router(field_router)
app.include_router(sensor_router)
app.include_router(measurement_router)
app.include_router(alert_router)
app.include_router(metrics_router)