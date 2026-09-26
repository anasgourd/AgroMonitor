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


router = APIRouter(
    prefix="/fields",
    tags=["Fields"]
)


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(
    field_id: int,
    db: Session = Depends(get_db)
):
    service = FieldService(db)

    field = service.get_field(field_id)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return field

@router.put("/{field_id}", response_model=FieldResponse)
def update_field(
    field_id: int,
    field_data: FieldUpdate,
    db: Session = Depends(get_db)
):
    service = FieldService(db)

    field = service.update_field(field_id, field_data)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return field

@router.delete("/{field_id}", status_code=204)
def delete_field(
    field_id: int,
    db: Session = Depends(get_db)
):
    service = FieldService(db)

    deleted = service.delete_field(field_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )
 
# These endpoints are nested under a field (/field/{sensor_id}/...)
# because the field is the parent resource of the sensor.            

@router.get("/{field_id}/sensors", response_model=list[SensorResponse])
def get_field_sensors(
    field_id: int,
    db: Session = Depends(get_db)
):
    service = SensorService(db)
    field_service = FieldService(db)

    sensors = service.get_field_sensors(field_id)
    field = field_service.get_field(field_id)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return sensors

@router.post(
    "/{field_id}/sensors",
    response_model=SensorResponse,
    status_code=201
)
def create_sensor(
    field_id: int,
    sensor_data: SensorCreate,
    db: Session = Depends(get_db)
) -> Sensor:

    service = SensorService(db)
    field_service = FieldService(db)

    field = field_service.get_field(field_id)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return service.create_sensor(field_id, sensor_data)

#endpoint for get alerts of the assosiated field
@router.get(
    "/{field_id}/alerts",
    response_model=list[AlertResponse]
)
def get_field_alerts(
    field_id: int,
    db: Session = Depends(get_db)
) -> list[AlertResponse]:

    field_service = FieldService(db)
    alert_service = AlertService(db)

    field = field_service.get_field(field_id)

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return alert_service.get_field_alerts(field_id)