import logging
import paho.mqtt.client as mqtt
import json
from app.schemas.measurement import MeasurementInput
from app.services.measurement_service import MeasurementService
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
from app.exceptions.measurement import SensorNotFoundError,InactiveSensorError,FutureMeasurementTimestampError
from sqlalchemy.exc import SQLAlchemyError
from app.metrics import mqtt_messages_received,mqtt_messages_rejected
import os
import ssl
logger = logging.getLogger(__name__)
import ssl

MAX_MQTT_PAYLOAD_BYTES = 4096


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
        self.topic = os.getenv("MQTT_CONSUMER_TOPIC", "agromonitor/sensors")

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )
        
        # MQTT Authentication
        self.client.username_pw_set(
            username=os.environ["MQTT_CONSUMER_USERNAME"],
            password=os.environ["MQTT_CONSUMER_PASSWORD"],
        )
        
        # MQTT TLS
        tls_enabled = (
            os.environ.get("MQTT_CONSUMER_TLS_ENABLED", "false").lower()
            == "true"
        )

        if tls_enabled:
            ca_cert = os.environ.get("MQTT_CONSUMER_CA_CERT") or None

            self.client.tls_set(
                ca_certs=ca_cert,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS_CLIENT,
            )
                

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info("Connected to MQTT broker")
            client.subscribe(self.topic, qos=0)
        else:
            logger.error("MQTT connection rejected: %s", reason_code)
    
    def on_disconnect(
        self, client, userdata, disconnect_flags,
        reason_code, properties
    ):
        if reason_code != 0:
            logger.warning("MQTT connection lost: %s", reason_code)
        else:
            logger.info("MQTT disconnected normally")

    def on_message(self, _client, _userdata, message):
        
        #Prometheus metric: Count total MQTT messages rejected by the broker/system
        mqtt_messages_received.inc()
        
        if len(message.payload) > MAX_MQTT_PAYLOAD_BYTES:
            mqtt_messages_rejected.inc()
            logger.warning("MQTT payload rejected: size limit exceeded")
            return
        
        try:
            payload = message.payload.decode()

        except UnicodeDecodeError:
            mqtt_messages_rejected.inc()
            
            logger.warning(
                "Invalid MQTT payload encoding"
            )
            return
        
        logger.info(
            "MQTT message received on topic %s",
            message.topic
        )
        
        #catching validation errors in the payload
        try:
            data = json.loads(payload)
            if not isinstance(data, dict):
                raise ValueError("MQTT payload must be a JSON object")
            #dictionary unpacking of the data of the payload to the measurement object
            measurement = MeasurementInput(**data)

        except (json.JSONDecodeError, ValidationError, ValueError):
            
            mqtt_messages_rejected.inc()
            
            logger.warning(
                "Invalid MQTT measurement payload"
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
            mqtt_messages_rejected.inc()
            logger.warning(
                "MQTT measurement rejected: sensor %s not found",
                measurement.sensor_id
            )

        except InactiveSensorError:
            mqtt_messages_rejected.inc()
            logger.warning(
                "MQTT measurement rejected: sensor %s is inactive",
                measurement.sensor_id
            )

        except FutureMeasurementTimestampError:
            mqtt_messages_rejected.inc()
            logger.warning(
                "MQTT measurement rejected: timestamp is in the future"
            )
        except SQLAlchemyError:
            mqtt_messages_rejected.inc()
            logger.exception(
                "Database error while processing MQTT measurement"
            )

        finally:
            db.close()

    def start(self):
        self.client.reconnect_delay_set(
            min_delay=1,
            max_delay=30
        )

        self.client.connect_async(
            self.broker,
            self.port,
            keepalive=60
        )

        self.client.loop_start()
    
    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()