from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.sensor import SensorResponse,SensorUpdate
from app.services.sensor_service import SensorService
from app.schemas.measurement import MeasurementResponse
from app.services.measurement_service import MeasurementService


router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse
)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
) -> SensorResponse:

    service = SensorService(db)

    sensor = service.get_sensor(sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return sensor

@router.put(
    "/{sensor_id}",
    response_model=SensorResponse
)
def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    db: Session = Depends(get_db)
) -> SensorResponse:

    service = SensorService(db)

    sensor = service.update_sensor(
        sensor_id,
        sensor_data
    )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return sensor

@router.delete(
    "/{sensor_id}",
    status_code=204
)
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
) -> None:

    service = SensorService(db)

    deleted = service.delete_sensor(sensor_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )
        
# These endpoints are nested under a sensor (/sensor/{measurement_id}/...)
# because the sensor is the parent resource of the measurement.       
@router.get(
    "/{sensor_id}/measurements",
    response_model=list[MeasurementResponse]
)
def get_sensor_measurements(
    sensor_id: int,
    db: Session = Depends(get_db)
) -> list[MeasurementResponse]:

    sensor_service = SensorService(db)
    measurement_service = MeasurementService(db)

    sensor = sensor_service.get_sensor(sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return measurement_service.get_sensor_measurements(sensor_id)
