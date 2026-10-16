from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.field import FieldResponse, FieldUpdate
from app.services.field_service import FieldService
from fastapi import HTTPException
from app.services.sensor_service import SensorService
from app.schemas.sensor import SensorResponse,SensorCreate
from app.models.sensor import Sensor
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService
from app.core.security import get_current_user_id

router = APIRouter(
    prefix="/fields",
    tags=["Fields"]
)


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(
    field_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = FieldService(db)
    field = service.get_field(field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Field not found")

    return field

@router.put("/{field_id}", response_model=FieldResponse)
def update_field(
    field_id: int,
    field_data: FieldUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = FieldService(db)
    field = service.get_field(field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Field not found")

    return service.update_field(field_id, field_data)

@router.delete("/{field_id}", status_code=204)
def delete_field(
    field_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = FieldService(db)
    field = service.get_field(field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Field not found")

    result = service.delete_field(field_id)

    if result == "has_sensors":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete field because it has associated sensors",
        )
 
# These endpoints are nested under a field (/field/{sensor_id}/...)
# because the field is the parent resource of the sensor.            

@router.get("/{field_id}/sensors", response_model=list[SensorResponse])
def get_field_sensors(
    field_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    field_service = FieldService(db)
    field = field_service.get_field(field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Field not found")

    sensor_service = SensorService(db)
    return sensor_service.get_field_sensors(field_id)

@router.post(
    "/{field_id}/sensors",
    response_model=SensorResponse,
    status_code=201,
)
def create_sensor(
    field_id: int,
    sensor_data: SensorCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> Sensor:
    field_service = FieldService(db)
    field = field_service.get_field(field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Field not found")

    sensor_service = SensorService(db)
    return sensor_service.create_sensor(field_id, sensor_data)


# GET alerts associated with a field
@router.get(
    "/{field_id}/alerts",
    response_model=list[AlertResponse]
)
def get_field_alerts(
    field_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> list[AlertResponse]:

    field_service = FieldService(db)
    field = field_service.get_field(field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    alert_service = AlertService(db)
    return alert_service.get_field_alerts(field_id)
