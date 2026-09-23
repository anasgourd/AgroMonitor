from app.core.database import SessionLocal
from app.logging_config import setup_logging
from app.mqtt.consumer import MQTTConsumer


# Entry point for running the MQTT consumer as a standalone process
def main():
    setup_logging()

    consumer = MQTTConsumer(
        broker="localhost",
        port=1883,
        session_factory=SessionLocal
    )

    try:
        consumer.start()

        # Keep the process alive while the MQTT loop
        # runs in the background.
        input("MQTT consumer running. Press Enter to stop...\n")

    finally:
        consumer.stop()


if __name__ == "__main__":
    main()