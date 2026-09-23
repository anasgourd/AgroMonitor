import json
import os
import paho.mqtt.publish as publish


BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "agromonitor/sensors"


def main():
    payload = {
        "sensor_id": 1,
        "value": 40,
        "timestamp": "2026-09-22T20:00:00Z",
        "unit": "C"
    }
    # payload = "invalid json"
    # payload = {
    # "sensor_id": 999,
    # "value": 24.5,
    # "timestamp": "2026-09-22T20:00:00Z",
    # "unit": "C"
    # }
    # payload = {
    #     "sensor_id": 24,
    #     "value": 24.5,
    #     "timestamp": "2026-09-22T20:00:00Z",
    #     "unit": "C"
    # }
    # payload = {
    #     "sensor_id": 1,
    #     "value": 24.5,
    #     "timestamp": "2030-01-01T20:00:00Z",
    #     "unit": "C"
    # }
    

    publish.single(
        TOPIC,
        payload=json.dumps(payload),
        hostname=BROKER,
        port=PORT
    )


if __name__ == "__main__":
    main()