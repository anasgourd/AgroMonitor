import json
from unittest.mock import MagicMock

from app.mqtt.consumer import MQTTConsumer
from app.exceptions.measurement import (
    SensorNotFoundError,
    InactiveSensorError,
    FutureMeasurementTimestampError,
)


def create_consumer():
    # Use a mock database because these tests focus on the MQTT consumer
    # and do not need a real database connection.
    db = MagicMock()

    consumer = MQTTConsumer(
        broker="localhost",
        port=1883,
        db=db
    )

    # Replace the real service with a mock so we can verify
    # how the consumer interacts with the MeasurementService.
    consumer.measurement_service = MagicMock()

    return consumer


def create_message(payload):
    # Create a mock MQTT message with the same attributes
    # that the consumer reads from a real Paho MQTT message.
    message = MagicMock()
    message.topic = "agromonitor/sensors"
    message.payload = payload.encode()

    return message


def test_valid_measurement_calls_service():
    consumer = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    message = create_message(json.dumps(payload))

    consumer.on_message(None, None, message)

    # A valid MQTT payload should reach the MeasurementService.
    consumer.measurement_service.record_measurement.assert_called_once()

    # Verify that the JSON payload was converted into the correct
    # MeasurementInput before being passed to the service.
    measurement = (
        consumer.measurement_service.record_measurement.call_args.args[0]
    )

    assert measurement.sensor_id == 1
    assert measurement.value == 24.5
    assert measurement.unit == "C"
    assert measurement.timestamp.isoformat() == "2026-09-22T20:00:00+00:00"


def test_invalid_json_is_rejected():
    consumer = create_consumer()

    message = create_message("invalid json")

    consumer.on_message(None, None, message)

    # Invalid JSON should be discarded before reaching the service.
    consumer.measurement_service.record_measurement.assert_not_called()


def test_non_object_json_is_rejected():
    consumer = create_consumer()

    message = create_message(json.dumps("invalid json"))

    consumer.on_message(None, None, message)

    # The MQTT payload must be a JSON object because MeasurementInput
    # is constructed using the object's fields.
    consumer.measurement_service.record_measurement.assert_not_called()


def test_invalid_measurement_payload_is_rejected():
    consumer = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5
    }

    message = create_message(json.dumps(payload))

    consumer.on_message(None, None, message)

    # Missing required MeasurementInput fields should prevent
    # the invalid measurement from reaching the service.
    consumer.measurement_service.record_measurement.assert_not_called()


def test_sensor_not_found_is_handled():
    consumer = create_consumer()

    payload = {
        "sensor_id": 999,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    # Simulate the business exception raised by the service
    # when the sensor does not exist.
    consumer.measurement_service.record_measurement.side_effect = (
        SensorNotFoundError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should handle the expected business exception
    # without allowing it to crash the MQTT processing loop.
    consumer.on_message(None, None, message)


def test_inactive_sensor_is_handled():
    consumer = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }

    # Simulate the business exception raised by the service
    # when the sensor is inactive.
    consumer.measurement_service.record_measurement.side_effect = (
        InactiveSensorError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should handle the rejection and remain operational.
    consumer.on_message(None, None, message)


def test_future_timestamp_is_handled():
    consumer = create_consumer()

    payload = {
        "sensor_id": 1,
        "value": 24.5,
        "timestamp": "2030-01-01T20:00:00Z",
        "unit": "C"
    }

    # Simulate the business exception raised by the service
    # when the measurement timestamp is in the future.
    consumer.measurement_service.record_measurement.side_effect = (
        FutureMeasurementTimestampError()
    )

    message = create_message(json.dumps(payload))

    # The consumer should handle the rejection without crashing.
    consumer.on_message(None, None, message)

