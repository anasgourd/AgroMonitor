import logging

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class MQTTConsumer:
    def __init__(self, broker: str, port: int):
        self.broker = broker
        self.port = port

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties):
        logger.info("Connected to MQTT broker")
        client.subscribe("agromonitor/sensors")

    def on_message(self, client, userdata, message):
        logger.info(
            "MQTT message received on topic %s: %s",
            message.topic,
            message.payload.decode()
        )

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_forever()