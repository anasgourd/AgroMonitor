import csv
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import paho.mqtt.publish as publish


BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "agromonitor/sensors"

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv"

DELAY_SECONDS = 0.01
MAX_MEASUREMENTS = None


def main():
    
    published_count = 0
    with open(DATA_FILE, newline="") as file:
        reader = csv.reader(file)

        for  row in reader:
            # if i >= MAX_MEASUREMENTS:
            #     break

            value = float(row[0])
            timestamp = datetime.now(timezone.utc)

            payload = {
                "sensor_id": 1,
                "value": value,
                "timestamp": timestamp.isoformat(),
                "unit": "C",
            }

            publish.single(
                TOPIC,
                payload=json.dumps(payload),
                hostname=BROKER,
                port=PORT,
            )
            published_count += 1
            #print(f"Published #{published_count}: {payload}")

            
            
            time.sleep(DELAY_SECONDS)
        print(f"Total published: {published_count}")


if __name__ == "__main__":
    main()