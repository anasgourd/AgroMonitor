from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.repositories.measurement_repository import MeasurementRepository


class MeasurementService:
    def __init__(self, db: Session):
        self.repository = MeasurementRepository(db)

    def get_sensor_measurements(
        self,
        sensor_id: int
    ) -> list[Measurement]:

        return self.repository.get_by_sensor_id(sensor_id)
    def get_measurement(
        self,
        measurement_id: int
    ) -> Measurement | None:

        return self.repository.get_by_id(measurement_id)