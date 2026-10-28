import csv
import json
import os
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
import ssl
import paho.mqtt.client as mqtt


BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_PUBLISHER_TOPIC", "agromonitor/sensors")
SENSOR_ID = int(os.getenv("MQTT_PUBLISHER_SENSOR_ID", "1"))


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv"

MAX_MEASUREMENTS = int(os.getenv("MAX_MEASUREMENTS", "10"))
DELAY_SECONDS = float(os.getenv("DELAY_SECONDS", "0.1"))
TIMESTAMP_INTERVAL_SECONDS = int(
    os.getenv("TIMESTAMP_INTERVAL_SECONDS", "0")
)

def main():
    if MAX_MEASUREMENTS < 0:
        raise ValueError("MAX_MEASUREMENTS must be non-negative")

    if DELAY_SECONDS < 0:
        raise ValueError("DELAY_SECONDS must be non-negative")

    if TIMESTAMP_INTERVAL_SECONDS < 0:
        raise ValueError("TIMESTAMP_INTERVAL_SECONDS must be non-negative")

    print(f"MQTT target: {BROKER}:{PORT}")
    print(f"MQTT topic: {TOPIC}")
    print(f"Sensor ID: {SENSOR_ID}")
    print(f"Timestamp interval: {TIMESTAMP_INTERVAL_SECONDS}s")

    client = mqtt.Client()
    client.username_pw_set(
        username=os.environ["MQTT_PUBLISHER_USERNAME"],
        password=os.environ["MQTT_PUBLISHER_PASSWORD"],
    )

    tls_enabled = (
        os.environ.get("MQTT_PUBLISHER_TLS_ENABLED", "false").lower() == "true"
    )

    if tls_enabled:
        ca_cert = os.environ.get("MQTT_PUBLISHER_CA_CERT") or None
        client.tls_set(
            ca_certs=ca_cert,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS_CLIENT,
        )

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        time.sleep(1)

        # Historical mode: all timestamps are in the past.
        start_timestamp = None

        if TIMESTAMP_INTERVAL_SECONDS > 0:
            start_timestamp = datetime.now(timezone.utc) - timedelta(
                seconds=MAX_MEASUREMENTS * TIMESTAMP_INTERVAL_SECONDS
            )

        published_count = 0

        with open(DATA_FILE, newline="") as file:
            reader = csv.reader(file)

            for i, row in enumerate(reader):
                if i >= MAX_MEASUREMENTS:
                    break

                value = float(row[0])

                if start_timestamp is not None:
                    timestamp = start_timestamp + timedelta(
                        seconds=i * TIMESTAMP_INTERVAL_SECONDS
                    )
                else:
                    timestamp = datetime.now(timezone.utc)

                payload = {
                    "sensor_id": SENSOR_ID,
                    "value": value,
                    "timestamp": timestamp.isoformat(),
                    "unit": "C",
                }

                result = client.publish(
                    TOPIC,
                    payload=json.dumps(payload),
                )
                result.wait_for_publish()

                published_count += 1
                print(f"Published #{published_count}: {payload}")

                time.sleep(DELAY_SECONDS)

        print(f"Total published: {published_count}")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
