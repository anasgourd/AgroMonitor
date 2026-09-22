from sqlalchemy.orm import Session
from app.models.measurement import Measurement
from app.repositories.measurement_repository import MeasurementRepository
from app.schemas.measurement import MeasurementInput

from app.services.sensor_service import SensorService
from datetime import datetime
from fastapi import HTTPException

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
    def record_measurement(
        self,
        measurement_data: MeasurementInput
    ) -> Measurement:
        sensor_service = SensorService(self.repository.db)
        sensor = sensor_service.get_sensor(measurement_data.sensor_id)

        if sensor is None:
            raise HTTPException(
                status_code=404,
            detail="Sensor not found"
        )
        if sensor.status != "active":
            raise HTTPException(
                status_code=400,
                detail="Sensor is inactive"
            )
        
        if measurement_data.timestamp > datetime.now():
            raise HTTPException(
                status_code=400,
                detail="Measurement timestamp cannot be in the future"
            )

        # Temporary anomaly detection
        is_anomalous = False

        return self.repository.create(
            measurement_data,
            is_anomalous
        )
        
        