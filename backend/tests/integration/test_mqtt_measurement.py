import json

from app.core.database import SessionLocal
from app.mqtt.consumer import MQTTConsumer
from app.models.alert import Alert
from app.models.measurement import Measurement

# Tests the complete MQTT flow for an anomalous measurement.
# The measurement should be stored as anomalous and an alert should be created.
def test_anomalous_mqtt_measurement_creates_alert():
    session = SessionLocal()

    try:
        consumer = MQTTConsumer(
            broker="localhost",
            port=1883,
            session_factory=SessionLocal,
        )

        payload = {
            "sensor_id": 1,
            "value": 35.0,
            "timestamp": "2026-09-22T20:00:00Z",
            "unit": "C",
        }

        message = type(
            "MQTTMessage",
            (),
            {
                "topic": "agromonitor/sensors",
                "payload": json.dumps(payload).encode(),
            },
        )()

        consumer.on_message(None, None, message)

        measurement = (
            session.query(Measurement)
            .filter(Measurement.sensor_id == 1)
            .order_by(Measurement.measurement_id.desc())
            .first()
        )

        assert measurement is not None
        assert measurement.value == 35.0
        assert measurement.is_anomalous is True

        alert = (
            session.query(Alert)
            .filter(
                Alert.measurement_id == measurement.measurement_id
            )
            .first()
        )

        assert alert is not None
        assert alert.message == "Anomaly detected"

    finally:
        session.close()

# Tests the complete MQTT flow for a normal measurement       
def test_normal_mqtt_measurement_creates_no_alert():
    session = SessionLocal()

    try:
        consumer = MQTTConsumer(
            broker="localhost",
            port=1883,
            session_factory=SessionLocal,
        )

        payload = {
            "sensor_id": 1,
            "value": 15.0,
            "timestamp": "2026-09-22T20:00:00Z",
            "unit": "C",
        }

        message = type(
            "MQTTMessage",
            (),
            {
                "topic": "agromonitor/sensors",
                "payload": json.dumps(payload).encode(),
            },
        )()

        consumer.on_message(None, None, message)

        measurement = (
            session.query(Measurement)
            .filter(Measurement.sensor_id == 1)
            .order_by(Measurement.measurement_id.desc())
            .first()
        )

        assert measurement is not None
        assert measurement.value == 15.0
        assert measurement.is_anomalous is False

        alert = (
            session.query(Alert)
            .filter(
                Alert.measurement_id == measurement.measurement_id
            )
            .first()
        )

        assert alert is None

    finally:
        session.close()