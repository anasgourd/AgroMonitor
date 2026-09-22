import logging
import paho.mqtt.client as mqtt
import json
from app.schemas.measurement import MeasurementInput
from app.services.measurement_service import MeasurementService
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class MQTTConsumer:
    def __init__(
        self,
        broker: str,
        port: int,
        db: Session
    ):
        self.broker = broker
        self.port = port
        self.db = db
        self.measurement_service = MeasurementService(db)

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

        data = json.loads(payload)
        #dictionary unpacking of the data of the payload to the measurement object
        measurement = MeasurementInput(**data)

        logger.info(
            "Measurement payload validated for sensor %s",
            measurement.sensor_id
        )
        #consumer calling the measurement service
        self.measurement_service.record_measurement(measurement)

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_forever()