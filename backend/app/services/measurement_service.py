from sqlalchemy.orm import Session
from app.models.measurement import Measurement
from app.repositories.measurement_repository import MeasurementRepository
from app.schemas.measurement import MeasurementInput

from app.services.sensor_service import SensorService
from datetime import datetime
from app.exceptions.measurement import (
    SensorNotFoundError,
    InactiveSensorError,
    FutureMeasurementTimestampError
)
import logging

logger = logging.getLogger(__name__)

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
            logger.warning(
                "Measurement rejected: sensor %s not found",
                measurement_data.sensor_id
            )
            raise SensorNotFoundError()
        
        if sensor.status != "active":
            logger.warning(
            "Measurement rejected: sensor %s is inactive",
            measurement_data.sensor_id
            )
            raise InactiveSensorError()
        
        if measurement_data.timestamp > datetime.now():
            logger.warning(
                "Measurement rejected: timestamp is in the future"
            )
            raise FutureMeasurementTimestampError()

        # Temporary anomaly detection
        is_anomalous = False

        measurement = self.repository.create(
            measurement_data,
            is_anomalous
        )

        logger.info(
            "Measurement %s stored successfully",
            measurement.measurement_id
        )

        return measurement
        
        