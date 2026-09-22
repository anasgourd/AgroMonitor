from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.measurement import MeasurementResponse,MeasurementInput
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

#temorary endpoint for checking the measurement input 
@router.post(
    "",
    response_model=MeasurementResponse,
    status_code=201
)
def record_measurement(
    measurement_data: MeasurementInput,
    db: Session = Depends(get_db)
) -> MeasurementResponse:
    service = MeasurementService(db)

    try:
        return service.record_measurement(measurement_data)

    except SensorNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    except InactiveSensorError:
        raise HTTPException(
            status_code=400,
            detail="Sensor is inactive"
        )

    except FutureMeasurementTimestampError:
        raise HTTPException(
            status_code=400,
            detail="Measurement timestamp cannot be in the future"
        )