from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementInput

class MeasurementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_sensor_id(
        self,
        sensor_id: int
    ) -> list[Measurement]:

        return (
            self.db.query(Measurement)
            .filter(Measurement.sensor_id == sensor_id)
            .all()
        )
    
    def get_by_id(
        self,
        measurement_id: int
    ) -> Measurement | None:

        return (
            self.db.query(Measurement)
            .filter(Measurement.measurement_id == measurement_id)
            .first()
        )
    
    def create(
        self,
        measurement_data: MeasurementInput,
        is_anomalous: bool
    ) -> Measurement:
        measurement = Measurement(
            sensor_id=measurement_data.sensor_id,
            value=measurement_data.value,
            timestamp=measurement_data.timestamp,
            unit=measurement_data.unit,
            is_anomalous=is_anomalous,
        )

        self.db.add(measurement)
        self.db.flush()

        return measurement