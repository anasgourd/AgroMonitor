# AgroMonitor — MQTT Technology Decisions

## 1. Overview

AgroMonitor uses the **MQTT protocol** to transmit measurements from IoT sensors to the backend system.

The following technology decisions were made for AgroMonitor V1, considering the current system requirements, operational simplicity, resource efficiency, and future extensibility.

## 2. MQTT Broker Selection — Eclipse Mosquitto

### Selected Technology

AgroMonitor V1 uses **Eclipse Mosquitto 2**, deployed as a dedicated service within Docker Compose.

### Why Mosquitto?

- **Lightweight:** Low CPU and memory consumption.
- **Native MQTT Support:** Specifically designed for MQTT publish/subscribe communication.
- **Operational Simplicity:** Straightforward installation, configuration, maintenance, and debugging.
- **Edge Compatibility:** Suitable for deployment on resource-constrained edge gateways close to physical sensors.
- **Portability:** Supports local development, Docker containers, Linux servers, and cloud deployments.
- **MQTT Capabilities:** Supports QoS 0/1/2, persistent sessions, retained messages, authentication, topic-based ACLs, and TLS.

### Alternatives Considered

| Technology | Primary Use Case | Reason Not Selected |
|---|---|---|
| **HiveMQ / EMQX** | Advanced MQTT infrastructure, broker management, and clustering | Distributed MQTT broker capabilities are not currently required. |
| **RabbitMQ** | Message queues, asynchronous tasks, and worker distribution | The current architecture does not require complex background jobs or independent task queues. |
| **Apache Kafka** | Distributed event streaming, event retention, and replay | Multiple streaming pipelines and historical event replay are not required in V1. |

These technologies are not necessarily mutually exclusive. For example, Mosquitto could handle sensor connectivity while Kafka supports downstream event processing in a future architecture.

### When to Reconsider

The broker selection may be revisited if the system requires distributed MQTT clustering, large-scale event streaming, asynchronous processing, or more advanced infrastructure management.

Any migration should be driven by **measured performance, reliability, and scalability requirements**, rather than sensor count alone.

## 3. MQTT Client Selection — Eclipse Paho-MQTT

### Selected Technology

AgroMonitor uses **Eclipse Paho-MQTT 2.x**, a Python MQTT client library, for communication with the broker.

Two primary MQTT clients are implemented:

- **Sensor Publisher:** Simulates IoT sensors and publishes JSON measurements to the `agromonitor/sensors` topic.
- **MQTT Consumer:** Subscribes to the same topic, receives incoming messages, and forwards them to the `MeasurementService` for validation, anomaly detection, and persistence.

### Why Paho-MQTT?

- **Python Integration:** Integrates directly with the existing Python backend.
- **Lightweight Implementation:** Requires no additional messaging infrastructure.
- **MQTT Protocol Support:** Supports MQTT 3.1.1/5, QoS levels, TLS, and authentication.
- **Callback-Based API:** Enables event-driven processing of incoming MQTT messages.
- **Portability:** Works in both local development and Docker environments.

## 4. MQTT Infrastructure & Security Decisions

The following infrastructure and security approaches were selected for AgroMonitor V1.

| Category | Selected Approach | Rationale |
|---|---|---|
| **Authentication & Authorization** | Username/Password + Topic-Based ACLs *(Planned)* | Separate publisher and consumer identities with restricted publish/subscribe permissions. |
| **Deployment** | Local Docker Compose | Simplifies development, debugging, integration testing, and internal service networking. |
| **Broker Implementation** | Eclipse Mosquitto 2 | Lightweight MQTT broker with low operational overhead. |
| **Management** | Self-hosted | Provides full control over broker configuration, networking, and security without depending on a managed provider. |
| **Transport & Security** | MQTT over TCP (port 1883) | Suitable for the current controlled local development environment. |

**Security Considerations:** MQTT over TCP without TLS does not encrypt transmitted measurements or credentials. Before connecting physical sensors over untrusted networks or exposing the broker publicly, TLS or another appropriately secured communication channel must be introduced.

Authentication and topic-based ACLs are part of the selected security approach but should be considered planned until their implementation is verified.