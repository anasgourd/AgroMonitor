# Record Measurements — MQTT Ingestion Design

## 1. Main Components

### MQTT Consumer

The MQTT Consumer receives measurement messages from the MQTT Broker and starts the measurement-processing workflow.

```python
def on_message(payload):
    data = parse_payload(payload)
    measurement_service.record_measurement(data)
```

Payload validation is performed before the data enters the main processing pipeline. Invalid or malformed payloads are logged and discarded.

### MeasurementService

The `MeasurementService` coordinates the processing of a measurement.

```python
def record_measurement(data):
    measurement = Measurement(
        sensor_id=data["sensor_id"],
        value=data["value"],
        unit=data["unit"],
        timestamp=data["timestamp"]
    )

    measurement.is_anomalous = (
        anomaly_detection_service.detect(measurement)
    )

    measurement_repository.save(measurement)
```

The service creates the measurement, requests anomaly detection, stores the anomaly result, and passes the measurement to the repository for persistence.

### AnomalyDetectionService

The `AnomalyDetectionService` coordinates anomaly detection using the configured strategy.

```python
def detect(measurement):
    return strategy.detect(measurement)
```

The service delegates the detection to the selected `AnomalyDetectionStrategy`.

### AnomalyDetectionStrategy

The Strategy Pattern allows different anomaly detection algorithms to be used without changing the `MeasurementService`.

```python
def detect(measurement):
    return model.predict(measurement)
```

The specific online anomaly detection model is not fixed at this stage. The model is stateful and may update its state as measurements are processed.

### MeasurementRepository

The Repository handles persistence of measurements and isolates database access from application logic.

```python
def save(measurement):
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
```

The Repository uses SQLAlchemy to persist the measurement in PostgreSQL.

### SQLAlchemy

SQLAlchemy maps the `Measurement` Python object to the corresponding database table and performs the database operation.

---

## 2. Analysis-to-Design Mapping

The LLD implementation is derived from the analysis models developed for the **Record Measurements** use case.

The BCE model identified the main responsibilities involved in the use case:

| Analysis component      | Design / Implementation component |
| ----------------------- | --------------------------------- |
| Sensor System           | Sensor + MQTT Broker              |
| MeasurementInput        | MQTT message / payload            |
| MeasurementController   | MQTT Consumer                     |
| AnomalyDetectionService | `AnomalyDetectionService`         |
| Measurement             | SQLAlchemy `Measurement` model    |

The BCE model helped identify the main responsibilities and interactions without introducing implementation details.

The sequence diagram then helped define the order of interactions between these responsibilities.

During LLD, these responsibilities were refined into concrete implementation components. In particular, `MeasurementService` was introduced to coordinate the application workflow, while `MeasurementRepository` isolates persistence from the service layer.

The analysis models therefore provided the conceptual structure, while the LLD translated that structure into concrete components and technologies.

---

## 3. Error Handling and Reliability

The MQTT Consumer handles errors that occur during message processing.

Malformed or invalid MQTT payloads are rejected before reaching the application services and are logged for troubleshooting.

The initial implementation uses synchronous processing and does not introduce a separate message queue or dead-letter queue.


### MQTT QoS

The initial implementation uses **MQTT QoS 0**, with higher QoS levels and application-level deduplication considered only if stronger delivery guarantees are required in the future.


---

## 4. Implementation Consideration

### Synchronous Anomaly Detection

Anomaly detection runs synchronously in the measurement write path by design. The measurement is analyzed before it is stored, so the `is_anomalous` result is available when the measurement is persisted.

This is a conscious trade-off for the initial implementation: a slow or failing anomaly detection model can delay or prevent measurement persistence. This is accepted for v1 in order to keep the processing flow simple and immediate.
