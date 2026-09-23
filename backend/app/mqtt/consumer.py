import logging
import paho.mqtt.client as mqtt
import json
from app.schemas.measurement import MeasurementInput
from app.services.measurement_service import MeasurementService
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
from app.exceptions.measurement import SensorNotFoundError,InactiveSensorError,FutureMeasurementTimestampError


logger = logging.getLogger(__name__)


class MQTTConsumer:
    def __init__(
        self,
        broker: str,
        port: int,
        session_factory: sessionmaker,
        service_factory=MeasurementService
    ):
        self.broker = broker
        self.port = port
        self.session_factory = session_factory
        self.service_factory = service_factory

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, reason_code, properties):
        logger.info("Connected to MQTT broker")
        client.subscribe("agromonitor/sensors")

    def on_message(self, client, userdata, message):
        payload = message.payload.decode()

        logger.info(
            "MQTT message received on topic %s: %s",
            message.topic,
            payload
        )
        
        #catching validation errors in the payload
        try:
            data = json.loads(payload)
            if not isinstance(data, dict):
                raise ValueError("MQTT payload must be a JSON object")
            #dictionary unpacking of the data of the payload to the measurement object
            measurement = MeasurementInput(**data)

        except (json.JSONDecodeError, ValidationError, ValueError):
            logger.warning(
                "Invalid MQTT measurement payload: %s",
                payload
            )
            return

        logger.info(
            "Measurement payload validated for sensor %s",
            measurement.sensor_id
        )
        
        db = self.session_factory()

        try:
            #consumer calling the measurement service
            measurement_service = self.service_factory(db)
            measurement_service.record_measurement(measurement)

        except SensorNotFoundError:
            logger.warning(
                "MQTT measurement rejected: sensor %s not found",
                measurement.sensor_id
            )

        except InactiveSensorError:
            logger.warning(
                "MQTT measurement rejected: sensor %s is inactive",
                measurement.sensor_id
            )

        except FutureMeasurementTimestampError:
            logger.warning(
                "MQTT measurement rejected: timestamp is in the future"
            )

        finally:
            db.close()

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
    
    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()