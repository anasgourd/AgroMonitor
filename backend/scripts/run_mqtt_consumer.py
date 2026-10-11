from app.core.database import SessionLocal
from app.logging_config import setup_logging
from app.mqtt.consumer import MQTTConsumer



def main():
    setup_logging()

    consumer = MQTTConsumer(
        broker="mqtt",
        port=1883,
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
