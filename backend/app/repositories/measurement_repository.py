from sqlalchemy.orm import Session

from app.models.measurement import Measurement


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