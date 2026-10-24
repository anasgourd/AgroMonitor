from fastapi import FastAPI

from app.api.user_router import router as user_router
from app.api.field_router import router as field_router
from app.api.sensor_router import router as sensor_router
from app.api.measurement_router import router as measurement_router
from app.api.alert_router import router as alert_router
from app.api.metrics_router import router as metrics_router
from app.api.auth_router import router as auth_router
from app.logging_config import setup_logging

from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.rate_limit import limiter

app = FastAPI(
    title="AgroMonitor API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

setup_logging()

app.include_router(user_router)
app.include_router(field_router)
app.include_router(sensor_router)
app.include_router(measurement_router)
app.include_router(alert_router)
app.include_router(metrics_router)
app.include_router(auth_router)