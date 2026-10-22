import json
from unittest.mock import MagicMock
from app.mqtt.consumer import MQTTConsumer
from app.exceptions.measurement import (
    SensorNotFoundError,
    InactiveSensorError,
    FutureMeasurementTimestampError,
)
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch
import logging
import ssl
import pytest

def create_consumer():

    # Use a mock database because these tests focus on the MQTT consumer
    # and do not need a real database connection.  
    db = MagicMock()
    session_factory = MagicMock(return_value=db)
    measurement_service = MagicMock()

    service_factory = MagicMock(
        return_value=measurement_service
    )

    consumer = MQTTConsumer(
        broker="localhost",
        port=1883,
        session_factory=session_factory,
        service_factory=service_factory
    )

    return consumer, measurement_service

def create_message(payload):
    # Create a mock MQTT message with the same attributes
    # that the consumer reads from a real Paho MQTT message.
    message = MagicMock()
    message.topic = "agromonitor/sensors"
    message.payload = payload.encode()

    return message


def test_valid_measurement_calls_service():
    consumer, measurement_service = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    message = create_message(json.dumps(payload))

    consumer.on_message(None, None, message)

    # A valid MQTT payload should reach the MeasurementService.
    measurement_service.record_measurement.assert_called_once()

    # Verify that the JSON payload was converted into the correct
    # MeasurementInput before being passed to the service.
    measurement = (
        measurement_service.record_measurement.call_args.args[0]
    )

    assert measurement.sensor_id == 1
    assert measurement.value == 24.5
    assert measurement.unit == "C"
    assert measurement.timestamp.isoformat() == "2026-09-22T20:00:00+00:00"


def test_invalid_json_is_rejected():
    consumer, measurement_service = create_consumer()

    message = create_message("invalid json")

    consumer.on_message(None, None, message)

    # Invalid JSON should be discarded before reaching the service.
    measurement_service.record_measurement.assert_not_called()


def test_non_object_json_is_rejected():
    consumer, measurement_service = create_consumer()

    message = create_message(json.dumps("invalid json"))

    consumer.on_message(None, None, message)

    # The MQTT payload must be a JSON object because MeasurementInput
    # is constructed using the object's fields.
    measurement_service.record_measurement.assert_not_called()


def test_invalid_measurement_payload_is_rejected():
    consumer, measurement_service = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5
    }

    message = create_message(json.dumps(payload))

    consumer.on_message(None, None, message)

    # Missing required MeasurementInput fields should prevent
    # the invalid measurement from reaching the service.
    measurement_service.record_measurement.assert_not_called()


def test_sensor_not_found_is_handled():
    consumer, measurement_service = create_consumer()

    payload = {
        "sensor_id": 999,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    # Simulate the business exception raised by the service
    # when the sensor does not exist.
    measurement_service.record_measurement.side_effect = (
        SensorNotFoundError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should handle the expected business exception
    # without allowing it to crash the MQTT processing loop.
    consumer.on_message(None, None, message)


def test_inactive_sensor_is_handled():
    consumer, measurement_service = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    # Simulate the business exception raised by the service
    # when the sensor is inactive.
    measurement_service.record_measurement.side_effect = (
        InactiveSensorError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should handle the rejection and remain operational.
    consumer.on_message(None, None, message)


def test_future_timestamp_is_handled():
    consumer, measurement_service = create_consumer()
    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2030-01-01T20:00:00Z",
        "unit": "C"
    }

    # Simulate the business exception raised by the service
    # when the measurement timestamp is in the future.
    measurement_service.record_measurement.side_effect = (
        FutureMeasurementTimestampError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should handle the rejection without crashing.
    consumer.on_message(None, None, message)

def test_database_error_is_handled():
    consumer, measurement_service = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    # Simulate a database error while storing the measurement.
    measurement_service.record_measurement.side_effect = (
        SQLAlchemyError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should catch the database error
    # without crashing the MQTT processing loop.
    consumer.on_message(None, None, message)

def test_database_session_is_closed():
    consumer, measurement_service = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    message = create_message(json.dumps(payload))

    consumer.on_message(None, None, message)

    db = consumer.session_factory.return_value

    # The database session should always be closed
    # after processing the MQTT message.
    db.close.assert_called_once()

def test_invalid_payload_encoding_is_rejected():
    consumer, measurement_service = create_consumer()

    message = MagicMock()
    message.topic = "agromonitor/sensors"
    message.payload = b"\xff\xfe\xfd"

    # Invalid UTF-8 payloads should be rejected
    # before reaching the measurement service.
    consumer.on_message(None, None, message)

    measurement_service.record_measurement.assert_not_called()
    

#for mqtt security tests

#Connection tests
def test_successful_connection_subscribes(caplog):
    consumer, _ = create_consumer()
    client = MagicMock()

    with caplog.at_level(logging.INFO):
        consumer.on_connect(client, None, None, 0, None)

    client.subscribe.assert_called_once_with(
        "agromonitor/sensors",
        qos=0
    )
    assert "Connected to MQTT broker" in caplog.text


def test_rejected_connection_does_not_subscribe(caplog):
    consumer, _ = create_consumer()
    client = MagicMock()

    with caplog.at_level(logging.ERROR):
        consumer.on_connect(client, None, None, 5, None)

    client.subscribe.assert_not_called()
    assert "MQTT connection rejected" in caplog.text
    
# Disconnection tests
def test_unexpected_disconnect_logs_warning(caplog):
    consumer, _ = create_consumer()

    with caplog.at_level(logging.WARNING):
        consumer.on_disconnect(
            MagicMock(), None, None, 1, None
        )

    assert "MQTT connection lost" in caplog.text


def test_normal_disconnect_logs_info(caplog):
    consumer, _ = create_consumer()

    with caplog.at_level(logging.INFO):
        consumer.on_disconnect(
            MagicMock(), None, None, 0, None
        )

    assert "MQTT disconnected normally" in caplog.text
    
# Start and stop tests


def test_start_configures_reconnection():
    consumer, _ = create_consumer()
    consumer.client = MagicMock()

    consumer.start()

    consumer.client.reconnect_delay_set.assert_called_once_with(
        min_delay=1,
        max_delay=30
    )

    consumer.client.connect_async.assert_called_once_with(
        "localhost",
        1883,
        keepalive=60
    )

    consumer.client.loop_start.assert_called_once()


def test_stop_disconnects_and_stops_loop():
    consumer, _ = create_consumer()
    consumer.client = MagicMock()

    consumer.stop()

    consumer.client.disconnect.assert_called_once()
    consumer.client.loop_stop.assert_called_once()
    
# TLS configuration tests


@pytest.mark.parametrize("tls_enabled", ["false", "true"])
def test_tls_configuration(tls_enabled):
    with patch.dict(
        "os.environ",
        {
            "MQTT_CONSUMER_USERNAME": "test_user",
            "MQTT_CONSUMER_PASSWORD": "test_password",
            "MQTT_CONSUMER_TLS_ENABLED": tls_enabled,
            "MQTT_CONSUMER_CA_CERT": "",
        }
    ):
        with patch("app.mqtt.consumer.mqtt.Client") as mock_client:
            MQTTConsumer(
                broker="localhost",
                port=1883,
                session_factory=MagicMock()
            )

            client = mock_client.return_value

            if tls_enabled == "true":
                client.tls_set.assert_called_once_with(
                    ca_certs=None,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLS_CLIENT
                )
            else:
                client.tls_set.assert_not_called()