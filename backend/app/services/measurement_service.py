from sqlalchemy.orm import Session
from app.models.measurement import Measurement
from app.repositories.measurement_repository import MeasurementRepository
from app.schemas.measurement import MeasurementInput

from app.services.sensor_service import SensorService
from datetime import datetime, timezone
from app.exceptions.measurement import (
    SensorNotFoundError,
    InactiveSensorError,
    FutureMeasurementTimestampError
)
import logging
from app.services.anomaly_detection.anomaly_detection_service import (
    AnomalyDetectionService,
)
from app.services.anomaly_detection.threshold_strategy import (
    ThresholdAnomalyDetectionStrategy,
)
from app.services.alert_service import AlertService

from app.metrics import measurements_stored, anomalies_detected
from app.metrics import alerts_created


logger = logging.getLogger(__name__)

class MeasurementService:
    def __init__(self, db: Session):
        self.repository = MeasurementRepository(db)
        self.anomaly_detector = AnomalyDetectionService(
            ThresholdAnomalyDetectionStrategy()
        )
        self.alert_service = AlertService(db)

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
    def record_measurement(self, measurement_data: MeasurementInput) -> Measurement:
        db = self.repository.db

        try:
            sensor_service = SensorService(db)
            sensor = sensor_service.get_sensor(measurement_data.sensor_id)

            if sensor is None:
                raise SensorNotFoundError()

            if sensor.status != "active":
                raise InactiveSensorError()

            if measurement_data.timestamp > datetime.now(timezone.utc):
                raise FutureMeasurementTimestampError()

            is_anomalous = self.anomaly_detector.is_anomalous(
                measurement_data.value
            )

            measurement = self.repository.create(
                measurement_data,
                is_anomalous
            )

            if is_anomalous:
                self.alert_service.create_alert(
                    measurement_id=measurement.measurement_id,
                    message="Anomaly detected",
                    timestamp=measurement.timestamp
                )

            # Save the ID before committing.
            measurement_id = measurement.measurement_id

            # Commit measurement and alert atomically.
            db.commit()

        except Exception:
            db.rollback()
            raise

        # Update metrics only after successful commit.
        measurements_stored.inc()

        if is_anomalous:
            anomalies_detected.inc()
            alerts_created.inc()

        logger.info(
            "Measurement %s stored successfully",
            measurement_id
        )

        return measurement
        
        