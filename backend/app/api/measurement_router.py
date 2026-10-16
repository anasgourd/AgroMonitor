from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.measurement import MeasurementResponse
from app.services.measurement_service import MeasurementService
from app.services.sensor_service import SensorService
from app.services.field_service import FieldService


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
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> MeasurementResponse:

    measurement_service = MeasurementService(db)
    measurement = measurement_service.get_measurement(measurement_id)

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail="Measurement not found"
        )

    sensor = SensorService(db).get_sensor(measurement.sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Measurement not found"
        )

    field = FieldService(db).get_field(sensor.field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(
            status_code=404,
            detail="Measurement not found"
        )

    return measurement