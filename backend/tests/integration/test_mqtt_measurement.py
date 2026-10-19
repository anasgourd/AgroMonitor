
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.mqtt.consumer import MQTTConsumer
from app.models.measurement import Measurement
from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.schemas.measurement import MeasurementInput
from app.services.measurement_service import MeasurementService


# Tests the complete MQTT flow for an anomalous measurement.
# The measurement should be stored as anomalous and an alert created.
def test_anomalous_mqtt_measurement_creates_alert(db_session):
    measurements_before = db_session.scalar(
        select(func.count()).select_from(Measurement)
    )
    alerts_before = db_session.scalar(
        select(func.count()).select_from(Alert)
    )

    consumer = MQTTConsumer(
        broker="localhost",
        port=1883,
        session_factory=SessionLocal,
    )

    payload = {
        "sensor_id": 1,
        "value": 85.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "unit": "C",
    }

    message = SimpleNamespace(
        topic="agromonitor/sensors",
        payload=json.dumps(payload).encode(),
    )

    consumer.on_message(None, None, message)

    # The consumer commits using a separate database session.
    db_session.expire_all()

    measurements_after = db_session.scalar(
        select(func.count()).select_from(Measurement)
    )
    alerts_after = db_session.scalar(
        select(func.count()).select_from(Alert)
    )

    assert measurements_after == measurements_before + 1
    assert alerts_after == alerts_before + 1

    measurement = db_session.scalar(
        select(Measurement)
        .where(Measurement.sensor_id == 1)
        .order_by(Measurement.measurement_id.desc())
        .limit(1)
    )

    assert measurement is not None
    assert measurement.value == 85.0
    assert measurement.is_anomalous is True

    alert = db_session.scalar(
        select(Alert).where(
            Alert.measurement_id == measurement.measurement_id
        )
    )

    assert alert is not None
    assert alert.message == "Anomaly detected"


# Tests the complete MQTT flow for a normal measurement.
# The measurement should be stored without creating an alert.
def test_normal_mqtt_measurement_creates_no_alert(db_session):
    measurements_before = db_session.scalar(
        select(func.count()).select_from(Measurement)
    )
    alerts_before = db_session.scalar(
        select(func.count()).select_from(Alert)
    )

    consumer = MQTTConsumer(
        broker="localhost",
        port=1883,
        session_factory=SessionLocal,
    )

    payload = {
        "sensor_id": 1,
        "value": 15.0,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "unit": "C",
    }

    message = SimpleNamespace(
        topic="agromonitor/sensors",
        payload=json.dumps(payload).encode(),
    )

    consumer.on_message(None, None, message)

    db_session.expire_all()

    measurements_after = db_session.scalar(
        select(func.count()).select_from(Measurement)
    )
    alerts_after = db_session.scalar(
        select(func.count()).select_from(Alert)
    )

    assert measurements_after == measurements_before + 1
    assert alerts_after == alerts_before

    measurement = db_session.scalar(
        select(Measurement)
        .where(Measurement.sensor_id == 1)
        .order_by(Measurement.measurement_id.desc())
        .limit(1)
    )

    assert measurement is not None
    assert measurement.value == 15.0
    assert measurement.is_anomalous is False

    alert = db_session.scalar(
        select(Alert).where(
            Alert.measurement_id == measurement.measurement_id
        )
    )

    assert alert is None


# Tests transaction rollback when alert creation fails.
# Neither the measurement nor the alert should be persisted.
def test_anomalous_measurement_rolls_back_when_alert_creation_fails(
    db_session,
    test_sensor,
    monkeypatch,
):
    measurement_data = MeasurementInput(
        sensor_id=test_sensor.sensor_id,
        value=85.0,
        timestamp=datetime.now(timezone.utc),
        unit="C",
    )

    measurements_before = db_session.scalar(
        select(func.count()).select_from(Measurement)
    )
    alerts_before = db_session.scalar(
        select(func.count()).select_from(Alert)
    )

    # Simulate an alert INSERT failure.
    def failing_create(self, *args, **kwargs):
        raise IntegrityError(
            "INSERT INTO alerts",
            {},
            Exception("Simulated alert insertion failure"),
        )

    monkeypatch.setattr(
        AlertRepository,
        "create",
        failing_create,
    )

    service = MeasurementService(db_session)

    with pytest.raises(IntegrityError):
        service.record_measurement(measurement_data)

    measurements_after = db_session.scalar(
        select(func.count()).select_from(Measurement)
    )
    alerts_after = db_session.scalar(
        select(func.count()).select_from(Alert)
    )

    assert measurements_after == measurements_before
    assert alerts_after == alerts_before
