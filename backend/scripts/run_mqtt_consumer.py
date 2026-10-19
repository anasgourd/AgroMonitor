from app.core.database import SessionLocal
from app.logging_config import setup_logging
from app.mqtt.consumer import MQTTConsumer
import os


def main():
    setup_logging()

    consumer = MQTTConsumer(
        broker=os.getenv("MQTT_BROKER", "mqtt"),
        port=int(os.getenv("MQTT_PORT", "1883")),
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
