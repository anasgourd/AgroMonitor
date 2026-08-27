# AgroMonitor — Functional Requirements

## 1. Purpose

This document defines the functional requirements of the AgroMonitor system.

AgroMonitor is a software platform for monitoring agricultural fields through
sensor data, historical analysis, machine learning and anomaly detection.


## 2. Scope

The initial system shall support:

- Field management and monitoring
- Sensor data collection
- Sensor data storage
- Historical data analysis
- Data visualization
- Machine learning inference
- Anomaly detection
- Alerts
- Field-level monitoring dashboard

Future extensions may include:

- Real-time IoT data ingestion
- Edge ML
- Distributed ML pipelines
- Generative AI capabilities
- Advanced automation


## 3. Functional Requirements

FR-01 — View Fields
The user shall be able to view all of their registered fields.

FR-02 — View Field Information
The user shall be able to select a specific field and view its information.

FR-03 — Add Field
The user shall be able to add a new field to their account.

FR-04 — Edit Field
The user shall be able to modify the information of an existing field.

FR-05 — Remove Field
The user shall be able to remove a field from their account.

FR-06 — Switch Between Fields
The user shall be able to switch between their registered fields.



FR-07 — View Sensors
The user shall be able to view the sensors associated with a selected field.

FR-08 — View Sensor Information
The user shall be able to view information about a specific sensor.

FR-09 — Add Sensor
The user shall be able to add a sensor to a field.

FR-10 — Edit Sensor
The user shall be able to modify the information of an existing sensor.

FR-11 — Remove Sensor
The user shall be able to remove a sensor from a field.


FR-12 — Record Measurements
The system shall record measurements produced by registered sensors.

FR-13 — Store Measurements
The system shall store each measurement together with its sensor, value, unit and timestamp.

FR-14 — Retrieve Measurements
The system shall allow the user to retrieve measurements for a selected sensor.

FR-15 — Visualize Measurements
The system shall visualize measurements over time.

FR-16 — View Latest Measurement
The system shall provide the latest available measurement for each sensor.

FR-17 — Measurement Validation
The system shall validate incoming measurements before storing them.