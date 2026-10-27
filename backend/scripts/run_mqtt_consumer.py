from app.core.database import SessionLocal
from app.logging_config import setup_logging
from app.mqtt.consumer import MQTTConsumer
import os
import signal
import threading
from prometheus_client import start_http_server


def main():
    setup_logging()

    shutdown_event = threading.Event()

    def request_shutdown(signum, frame):
        shutdown_event.set()

    signal.signal(signal.SIGTERM, request_shutdown)
    signal.signal(signal.SIGINT, request_shutdown)

    consumer = MQTTConsumer(
        broker=os.environ["MQTT_CONSUMER_HOST"],
        port=int(os.environ.get("MQTT_CONSUMER_PORT", "1883")),
        session_factory=SessionLocal
    )
    
    metrics_port = int(os.getenv("METRICS_PORT", "8001"))
    start_http_server(metrics_port, addr="0.0.0.0")

    try:
        consumer.start()
        shutdown_event.wait()
    finally:
        consumer.stop()


if __name__ == "__main__":
    main()
