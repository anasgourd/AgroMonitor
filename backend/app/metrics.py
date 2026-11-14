from prometheus_client import Counter


mqtt_messages_received = Counter(
    "agromonitor_mqtt_messages_received_total",
    "Total number of MQTT messages received",
)

mqtt_messages_rejected = Counter(
    "agromonitor_mqtt_messages_rejected_total",
    "Total number of MQTT messages rejected",
)

measurements_stored = Counter(
    "agromonitor_measurements_stored_total",
    "Total number of measurements stored",
)

anomalies_detected = Counter(
    "agromonitor_anomalies_detected_total",
    "Total number of anomalies detected",
)

alerts_created = Counter(
    "agromonitor_alerts_created_total",
    "Total number of alerts created",
)