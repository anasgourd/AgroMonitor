# AgroMonitor — API Design

## 1. Overview

The AgroMonitor backend exposes a REST API for interacting with the main system resources.

The main resources are:

* User
* Field
* Sensor
* Measurement
* Alert

The REST API is primarily used by the frontend, while sensor measurements are received through MQTT.

Authentication is outside the scope of the current API implementation.

All endpoints under `/users/{user_id}/...`, `/fields/...`,
`/sensors/...`, `/measurements/...`, and `/alerts/...` are considered
protected and will require authentication once authentication is implemented.

Authorization will ensure that an authenticated user can only access
resources they are allowed to access.


### Pagination and Filtering

List endpoints support pagination and filtering where needed.

For measurement history, time-range filtering and result limits are
particularly important because the number of measurements can grow
significantly.

Example:
GET /sensors/{sensor_id}/measurements?from=...&to=...&limit=...
---

# 2. User

### Data Model

```text
User
- user_id: Integer (PK)
- username : String
- fullname: String
- password: String
```

### Endpoints

| Method | Endpoint           | Purpose                  |
| ------ | ------------------ | ------------------------ |
| GET    | `/users/{user_id}` | Retrieve a specific user |
| POST   | `/users`           | Create a new user        |
| PUT    | `/users/{user_id}` | Update a user            |
| DELETE | `/users/{user_id}` | Delete a user            |

---

# 3. Field

### Data Model

```text
Field
- field_id: Integer (PK)
- user_id: Integer (FK)
- field_name: String
- type: String
- area: Float
```

A Field belongs to a User.

### Endpoints

| Method | Endpoint                  | Purpose                       |
| ------ | ------------------------- | ----------------------------- |
| GET    | `/users/{user_id}/fields` | Retrieve all fields of a user |
| POST   | `/users/{user_id}/fields` | Create a new field            |
| GET    | `/fields/{field_id}`      | Retrieve a specific field     |
| PUT    | `/fields/{field_id}`      | Update a field                |
| DELETE | `/fields/{field_id}`      | Delete a field                |

---

# 4. Sensor

### Data Model

```text
Sensor
- sensor_id: Integer (PK)
- field_id: Integer (FK)
- sensor_name: String
- status: String
```

A Sensor belongs to a Field.

### Endpoints

| Method | Endpoint                     | Purpose                         |
| ------ | ---------------------------- | ------------------------------- |
| GET    | `/fields/{field_id}/sensors` | Retrieve all sensors of a field |
| POST   | `/fields/{field_id}/sensors` | Create a new sensor             |
| GET    | `/sensors/{sensor_id}`       | Retrieve a specific sensor      |
| PUT    | `/sensors/{sensor_id}`       | Update a sensor                 |
| DELETE | `/sensors/{sensor_id}`       | Delete a sensor                 |

---

# 5. Measurement

### Data Model

```text
Measurement
- measurement_id: Integer (PK)
- sensor_id: Integer (FK → Sensor.sensor_id)
- value: Float
- timestamp: DateTime
- unit: String
- is_anomalous: Boolean
```

A Measurement belongs to a Sensor.

### Endpoints

| Method | Endpoint                            | Purpose                           |
| ------ | ----------------------------------- | --------------------------------- |
| GET    | `/sensors/{sensor_id}/measurements` | Retrieve measurements of a sensor |
| GET    | `/measurements/{measurement_id}`    | Retrieve a specific measurement   |

Measurements are not created through the REST API. They enter the system through the MQTT processing pipeline.

---

# 6. Alert

### Data Model

```text
Alert
- alert_id (PK)
- measurement_id (FK)
- message: String
- timestamp: DateTime
```

An Alert is generated from an anomalous Measurement; its associated Field is derived via Measurement → Sensor → Field.

### Endpoints

| Method | Endpoint                    | Purpose                                               |
| ------ | --------------------------- | ----------------------------------------------------- |
| `GET`  | `/users/{user_id}/alerts`   | Retrieve all alerts associated with the user's fields |
| `GET`  | `/fields/{field_id}/alerts` | Retrieve alerts associated with a specific field      |
| `GET`  | `/alerts/{alert_id}`        | Retrieve a specific alert                             |


Alerts are generated internally by the anomaly analysis process and are not created through the REST API.


