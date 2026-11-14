from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.sensor import SensorResponse,SensorUpdate
from app.services.sensor_service import SensorService
from app.schemas.measurement import MeasurementResponse
from app.services.measurement_service import MeasurementService
from app.services.field_service import FieldService
from app.core.security import get_current_user_id

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)


def get_owned_sensor(
    sensor_id: int,
    current_user_id: int,
    db: Session
):
    sensor = SensorService(db).get_sensor(sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    field = FieldService(db).get_field(sensor.field_id)
    # A sensor belongs to a field, so we check ownership through its parent field.

    if field is None or field.user_id != current_user_id:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return sensor


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse
)
def get_sensor(
    sensor_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> SensorResponse:

    return get_owned_sensor(sensor_id, current_user_id, db)

@router.put(
    "/{sensor_id}",
    response_model=SensorResponse
)
def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> SensorResponse:

    get_owned_sensor(sensor_id, current_user_id, db)

    sensor = SensorService(db).update_sensor(
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
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> None:

    get_owned_sensor(sensor_id, current_user_id, db)

    result = SensorService(db).delete_sensor(sensor_id)

    if result == "not_found":
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    if result == "has_measurements":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete sensor because it has recorded measurements"
        )
        
# These endpoints are nested under a sensor (/sensor/{measurement_id}/...)
# because the sensor is the parent resource of the measurement.       
@router.get(
    "/{sensor_id}/measurements",
    response_model=list[MeasurementResponse]
)
def get_sensor_measurements(
    sensor_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> list[MeasurementResponse]:

    get_owned_sensor(sensor_id, current_user_id, db)

    measurement_service = MeasurementService(db)

    return measurement_service.get_sensor_measurements(sensor_id)
