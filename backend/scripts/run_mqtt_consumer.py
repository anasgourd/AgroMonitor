from app.core.database import SessionLocal
from app.logging_config import setup_logging
from app.mqtt.consumer import MQTTConsumer

# Entry point for running the MQTT consumer as a standalone process
def main():
    setup_logging()

    db = SessionLocal()

    try:
        consumer = MQTTConsumer(
            broker="localhost",
            port=1883,
            db=db
        )

        consumer.start()
    finally:
        db.close()


if __name__ == "__main__":
    main()