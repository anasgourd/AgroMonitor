# Use Case Specifications

## UC-01 — View Fields

### Main Success Scenario

1. The Farmer accesses the fields view.
2. The system retrieves the fields associated with the Farmer's account.
3. The system displays the registered fields.

### Alternative / Exception Flows

- If no fields are registered, the system informs the Farmer that no fields are available.

### Traceability

FR-01

---

## UC-02 — View Field Information

### Main Success Scenario

1. The Farmer views the list of registered fields.
2. The Farmer selects a field.
3. The system retrieves the information associated with the selected field.
4. The system displays the field information.

### Alternative / Exception Flows

- If the selected field cannot be found, the system informs the Farmer that the field is unavailable.

### Traceability

FR-02

---

## UC-03 — Manage Field

### Main Success Scenario

1. The Farmer selects the field management functionality.
2. The Farmer selects the desired operation: add, edit, or remove a field.
3. The system performs the selected operation.
4. The system confirms the successful completion of the operation.

### Alternative / Exception Flows

- If the provided field information is invalid or incomplete, the system informs the Farmer and requests correction.
- If the selected field cannot be found or accessed, the system informs the Farmer that the field is unavailable.
- If the operation cannot be completed, the system informs the Farmer that the operation was unsuccessful.

### Traceability

FR-03, FR-04, FR-05

---

## UC-04 — View Sensors

### Preconditions

1. The Farmer has selected a field.

### Main Success Scenario

1. The Farmer accesses the sensors associated with the selected field.
2. The system retrieves the sensors associated with the selected field.
3. The system displays the available sensors.

### Alternative / Exception Flows

- If no sensors are associated with the selected field, the system informs the Farmer that no sensors are available.
- If the selected field cannot be found or accessed, the system informs the Farmer that the field is unavailable.

### Traceability

FR-06

---

## UC-05 — View Sensor Information

### Preconditions

1. The Farmer has selected a field.

### Main Success Scenario

1. The Farmer selects a sensor associated with the selected field.
2. The system retrieves the sensor information.
3. The system displays the sensor information.

### Alternative / Exception Flows

- If the selected sensor cannot be found or accessed, the system informs the Farmer that the sensor is unavailable.

### Traceability

FR-07

---

## UC-06 — Manage Sensors

### Preconditions

1. The Farmer has selected a field.

### Main Success Scenario

1. The Farmer accesses the sensor management functionality.
2. The Farmer selects the desired operation: add, edit, or remove a sensor.
3. The system performs the selected operation.
4. The system confirms the successful completion of the operation.

### Alternative / Exception Flows

- If the provided sensor information is invalid or incomplete, the system informs the Farmer and requests correction.

- If the selected sensor cannot be found or accessed, the system informs the Farmer that the sensor is unavailable.

- If the operation cannot be completed, the system informs the Farmer that the operation was unsuccessful.

### Traceability

FR-08, FR-09, FR-10

---

## UC-07 — View Measurements

### Preconditions

1. The Farmer has selected a sensor.

### Main Success Scenario

1. The Farmer accesses the measurements associated with the selected sensor.
2. The system retrieves the measurements associated with the selected sensor.
3. The system displays the available measurements.

### Alternative / Exception Flows

- If no measurements are available for the selected sensor, the system informs the Farmer that no measurements are available.

- If the selected sensor cannot be found or accessed, the system informs the Farmer that the sensor is unavailable.

### Traceability

FR-11

---

## UC-08 — View Alerts

### Main Success Scenario

1. The Farmer accesses the alerts functionality.
2. The system retrieves the alerts associated with the Farmer's fields.
3. The system displays the available alerts.

### Alternative / Exception Flows

- If no alerts are available, the system informs the Farmer that there are no alerts to display.

### Traceability

FR-12

---

## UC-09 — Record Measurements

### Main Success Scenario

1. The registered Sensor sends a new measurement value to the system. (FR-13)
2. The system validates the incoming measurement. (FR-15)
3. The system analyzes the measurement to detect potential operational anomalies. (FR-16)
4. The system stores the measurement together with the sensor identifier, value, unit, and timestamp. (FR-14)
5. The system completes the measurement recording process.

### Alternative / Exception Flows

**2a. Validation Fails**

- If the incoming measurement is invalid or corrupted, the system rejects the measurement.
- The system does not store the measurement.

**3a. Anomaly Detected**

- If the system detects an anomaly in the measurement, the system stores the measurement and marks it as anomalous. (FR-14, FR-16)
- The system triggers UC-10 — Generate Alerts. (FR-17)

### Traceability

FR-13, FR-14, FR-15, FR-16

---

## UC-10 — Generate Alerts

### Main Success Scenario

1. The system detects an anomaly in a measurement.
2. The system generates an alert containing information about the detected anomaly.
3. The system makes the alert available to the Farmer.

### Alternative / Exception Flows

- If the alert cannot be generated, the system does not make the alert available to the Farmer.

### Traceability

FR-17