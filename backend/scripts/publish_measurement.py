import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt


BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "agromonitor/sensors"

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv"

DELAY_SECONDS = 0.1
MAX_MEASUREMENTS = 10


def main():
    published_count = 0

    client = mqtt.Client()
    client.username_pw_set(
    username=os.environ["MQTT_PUBLISHER_USERNAME"],
    password=os.environ["MQTT_PUBLISHER_PASSWORD"],
    )
    client.connect(BROKER, PORT, 60)
    
    client.loop_start()

    # Wait briefly for the broker's authentication response
    time.sleep(1)

    with open(DATA_FILE, newline="") as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i >= MAX_MEASUREMENTS:
                break

            value = float(row[0])
            timestamp = datetime.now(timezone.utc)

            payload = {
                "sensor_id": 1,
                "value": value,
                "timestamp": timestamp.isoformat(),
                "unit": "C",
            }

            client.publish(
                TOPIC,
                payload=json.dumps(payload),
            )

            published_count += 1
            print(f"Published #{published_count}: {payload}")

            time.sleep(DELAY_SECONDS)

    client.disconnect()
    client.loop_stop()

    print(f"Total published: {published_count}")


if __name__ == "__main__":
    main()