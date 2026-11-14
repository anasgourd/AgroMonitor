# System Architecture

## 1. System Overview

The AgroMonitor system consists of two main deployable components:

1. Frontend
2. Backend

The backend handles both REST API requests and MQTT-based sensor data
stream processing.

The frontend communicates with the backend through a REST API.

The backend receives sensor data through an MQTT-based data stream. A
dedicated MQTT consumer component, running within the backend, subscribes
to sensor topics, validates incoming data, handles duplicate messages,
and passes valid measurements to the application layer for processing
and persistence.

### Why this architecture?

This separation allows the user interface, application logic, and
sensor-data processing responsibilities to evolve independently.

REST is used for request-response interactions between the frontend and
backend, while MQTT is used for asynchronous sensor-data communication.

This keeps the architecture simple while providing a natural
communication model for each type of interaction.

---

## 2. Technology Stack

Describe the main technologies and their roles:

- React / Vite — frontend
- FastAPI / Python — backend API
- PostgreSQL — persistent storage
- MQTT — sensor data communication
- Docker — containerization
- Prometheus / Grafana — observability
- CI/CD — automated testing and deployment

The selected technologies are lightweight, widely used, and appropriate
for the current scale and requirements of the system.

---

## 3. Architectural Style

AgroMonitor follows a layered architecture implemented as a modular
monolith.

### Layers

- Presentation / API layer
- Application / Service layer
- Domain layer
- Persistence layer

MQTT-based stream processing is implemented as an internal backend
responsibility rather than as a separate deployable service. The MQTT
consumer receives sensor messages and passes validated measurements to
the application layer.

### Why a modular monolith?

A modular monolith was selected instead of microservices because the
current system does not require independent service deployment or the
operational complexity of a distributed microservice architecture.

The system is still divided into clear modules, allowing individual
responsibilities to remain separated while keeping deployment and
development simple.

This also leaves the system open to future extraction of specific
modules into independent services if required.

---

## 4. Gateway and Deployment Platform

The initial deployment uses a managed PaaS (Render).

In this deployment, TLS termination and request routing are handled
by Render's managed platform gateway. A dedicated reverse proxy (e.g.
Nginx or Traefik) is not required at this stage but may be introduced
if the system migrates to self-managed infrastructure.

### Why?

The goal at this stage is to achieve a simple and reproducible
deployment without introducing unnecessary infrastructure management.

The PaaS approach allows the project to focus on application and
system design rather than infrastructure administration, while still
providing a single, secure entry point to the application.

---

## 5. Containerization and CI/CD

Docker is used to package the application and its dependencies into
reproducible environments.

CI/CD automates:

- building
- testing
- validation
- deployment

This reduces environment-specific problems and provides a repeatable
path from source code to deployment.

---

## 6. Observability

The initial observability solution intentionally remains simple.

### Logging

Python's built-in `logging` module is used for application logs.

### Metrics

Prometheus is used to collect application/system metrics.

### Visualization

Grafana is used to visualize metrics and support monitoring.

### Why?

The project requires visibility into failures and system behaviour,
but does not currently justify a complex observability stack.

The selected tools provide the necessary logging and metrics
capabilities while keeping the operational overhead relatively low.

---

## 7. Persistence Layer

Persistence is separated from the application/domain logic through a
dedicated persistence layer.

A repository-based abstraction can be used to isolate database access
from the rest of the application.

The application therefore depends on persistence abstractions rather
than directly coupling business logic to PostgreSQL-specific access
code.

### Why?

This improves separation of concerns and makes the persistence
implementation easier to test, change and evolve.

The persistence design should remain as simple as possible at the
current stage. ORM usage, query strategies and other database-specific
decisions are implementation concerns and are described in the LLD
documentation where appropriate.

---

## 8. Authentication and Authorization

Authentication is handled via JWT-based tokens issued by the backend
after credential validation. Authorization is enforced at the API
layer based on user roles (e.g. farmer, admin), restricting access to
fields and sensors owned by the authenticated user.

### Why?

JWT-based authentication is stateless and integrates naturally with a
REST API, avoiding the need for server-side session storage.

Role-based authorization at the API layer keeps access control
centralized and consistent across all modules. Detailed implementation
(token structure, expiry, refresh strategy) is covered in the LLD
documentation.

---
## 9. Machine Learning and Stream Processing

AgroMonitor uses online anomaly detection for incoming sensor data.

Each validated and deduplicated measurement is processed by the anomaly
detection model as it arrives rather than waiting for measurements to
accumulate into batches.

The processing flow is:

Sensor → MQTT Broker → MQTT Consumer → Validation / Deduplication
→ Online Anomaly Detection → Persistence → Alert Generation

The anomaly detection model is stateful and may maintain information
from previous measurements as part of its online processing.

Batch processing is not used for the primary real-time anomaly
detection path. It may be introduced separately for historical
analysis or model retraining.

### Why?

Online processing is appropriate for AgroMonitor because anomalies
should be detected close to the time at which sensor measurements are
received.

Keeping the ML processing in the existing backend also avoids
introducing a separate ML service at the current scale.

---

### 10.MQTT QoS and Duplicate Handling

The initial implementation uses MQTT QoS 0 because the system operates with a small, controlled simulated sensor workload. QoS 0 does not guarantee message delivery, but the initial system accepts this risk in exchange for lower protocol overhead and simpler processing. The expected message volume and controlled environment make occasional message loss an acceptable trade-off for the initial implementation.

If the system is later deployed at larger scale or measurement delivery becomes a stricter reliability requirement, MQTT QoS 1 can be introduced. QoS 1 provides at-least-once delivery but allows the same message to be delivered more than once.

Duplicate delivery is particularly relevant for AgroMonitor because measurements are processed by the online anomaly detection model as they arrive. Since the model is stateful and may update its learned state from incoming measurements, processing the same measurement more than once could affect the model's state and learning behaviour. It could also cause repeated anomaly detection or duplicate alert generation.

Application-level deduplication can then be introduced when the MQTT payload contract is defined. The exact deduplication mechanism will depend on how the sensor messages identify individual measurements. This keeps the initial implementation simple without committing the current database design to additional message-identity fields or infrastructure before they are required.


---



## 11. Future Scalability and Evolution

The initial architecture deliberately avoids premature complexity.

As the system grows, the following improvements could be introduced:

- Redis for caching
- asynchronous data-stream processing using a queue or stream
- Kubernetes for container orchestration and scaling

These are considered possible evolution paths rather than requirements
of the current implementation.