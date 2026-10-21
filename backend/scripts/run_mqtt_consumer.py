from app.core.database import SessionLocal
from app.logging_config import setup_logging
from app.mqtt.consumer import MQTTConsumer
import os


def main():
    setup_logging()
    
    host = os.environ["MQTT_CONSUMER_HOST"]
    port = int(os.environ.get("MQTT_CONSUMER_PORT", "1883"))

    consumer = MQTTConsumer(
        broker=host,
        port=port,
        session_factory=SessionLocal
    )

    try:
        consumer.start()

        # Keep the consumer process alive.
        import threading
        threading.Event().wait()

    finally:
        consumer.stop()


if __name__ == "__main__":
    main()
