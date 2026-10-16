
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService
from app.services.measurement_service import MeasurementService
from app.services.sensor_service import SensorService
from app.services.field_service import FieldService


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
def get_alert(
    alert_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> AlertResponse:
    alert = AlertService(db).get_alert(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    measurement = MeasurementService(db).get_measurement(
        alert.measurement_id
    )

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    sensor = SensorService(db).get_sensor(measurement.sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    field = FieldService(db).get_field(sensor.field_id)

    if field is None or field.user_id != current_user_id:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert
