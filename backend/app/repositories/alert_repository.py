from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.measurement import Measurement
from app.models.sensor import Sensor
from app.models.field import Field
from datetime import datetime


class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(
        self,
        user_id: int
    ) -> list[Alert]:

        return (
            self.db.query(Alert)
            .join(
                Measurement,
                Alert.measurement_id == Measurement.measurement_id
            )
            .join(
                Sensor,
                Measurement.sensor_id == Sensor.sensor_id
            )
            .join(
                Field,
                Sensor.field_id == Field.field_id
            )
            .filter(Field.user_id == user_id)
            .all()
        )
        
    def get_by_field_id(
        self,
        field_id: int
    ) -> list[Alert]:

        return (
            self.db.query(Alert)
            .join(
                Measurement,
                Alert.measurement_id == Measurement.measurement_id
            )
            .join(
                Sensor,
                Measurement.sensor_id == Sensor.sensor_id
            )
            .filter(Sensor.field_id == field_id)
            .all()
        )
    
    def get_by_id(
        self,
        alert_id: int
    ) -> Alert | None:
        
        return (
            self.db.query(Alert)
            .filter(Alert.alert_id == alert_id)
            .first()
        )

    def create(
        self,
        measurement_id: int,
        message: str,
        timestamp: datetime
    ) -> Alert:

        alert = Alert(
            measurement_id=measurement_id,
            message=message,
            timestamp=timestamp
        )

        self.db.add(alert)
        self.db.flush()

        return alert