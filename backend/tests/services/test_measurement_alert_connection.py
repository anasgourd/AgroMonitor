from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementInput
from app.services.measurement_service import MeasurementService


def create_measurement_service():
    db = MagicMock()
    service = MeasurementService(db)

    service.repository = MagicMock()
    service.alert_service = MagicMock()

    return service


def test_normal_measurement_creates_no_alert():
    service = create_measurement_service()

    sensor = MagicMock()
    sensor.status = "active"

    measurement_data = MeasurementInput(
        sensor_id=1,
        value=25.0,
        timestamp=datetime.now(timezone.utc),
        unit="C",
    )

    measurement = Measurement(
        measurement_id=1,
        sensor_id=1,
        value=25.0,
        timestamp=measurement_data.timestamp,
        unit="C",
        is_anomalous=False,
    )

    service.repository.create.return_value = measurement

    with patch(
        "app.services.measurement_service.SensorService"
    ) as sensor_service_class:

        sensor_service_class.return_value.get_sensor.return_value = sensor

        result = service.record_measurement(measurement_data)

    assert result.is_anomalous is False
    service.alert_service.create_alert.assert_not_called()


def test_anomalous_measurement_creates_one_alert():
    service = create_measurement_service()

    sensor = MagicMock()
    sensor.status = "active"

    measurement_data = MeasurementInput(
        sensor_id=1,
        value=35.0,
        timestamp=datetime.now(timezone.utc),
        unit="C",
    )

    measurement = Measurement(
        measurement_id=1,
        sensor_id=1,
        value=35.0,
        timestamp=measurement_data.timestamp,
        unit="C",
        is_anomalous=True,
    )

    service.repository.create.return_value = measurement
    # Temporarily replaces SensorService with a mock so the test
    # can control the sensor response without accessing the database    
    with patch(
        "app.services.measurement_service.SensorService"
    ) as sensor_service_class:

        sensor_service_class.return_value.get_sensor.return_value = sensor

        result = service.record_measurement(measurement_data)

    assert result.is_anomalous is True

    service.alert_service.create_alert.assert_called_once_with(
        measurement_id=1,
        message="Anomaly detected",
        timestamp=measurement_data.timestamp,
    )