from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.measurement import MeasurementResponse
from app.services.measurement_service import MeasurementService
from app.exceptions.measurement import (
    SensorNotFoundError,
    InactiveSensorError,
    FutureMeasurementTimestampError
)

router = APIRouter(
    prefix="/measurements",
    tags=["Measurements"]
)


@router.get(
    "/{measurement_id}",
    response_model=MeasurementResponse
)
def get_measurement(
    measurement_id: int,
    db: Session = Depends(get_db)
) -> MeasurementResponse:

    service = MeasurementService(db)

    measurement = service.get_measurement(measurement_id)

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail="Measurement not found"
        )

    return measurement

