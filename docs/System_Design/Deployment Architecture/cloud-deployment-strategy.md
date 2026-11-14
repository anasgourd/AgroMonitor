# AgroMonitor — Cloud Deployment Strategy

**Status:** Implemented — Software V1

## 1. Overview

AgroMonitor V1 uses a hybrid cloud and local deployment architecture.

The React frontend and FastAPI backend are hosted on Render, while Neon PostgreSQL provides managed cloud database storage.

The MQTT infrastructure remains local, using Eclipse Mosquitto and dedicated MQTT consumers running in Docker containers. A separate cloud consumer connects to Neon PostgreSQL to persist incoming sensor measurements.

This approach provides a publicly accessible web application while preserving the existing Docker-based MQTT infrastructure.

The deployment strategy prioritizes simplicity, low infrastructure overhead, and reuse of the existing application architecture.

## 2. Deployment Architecture

| Component | Deployment | Technology |
|---|---|---|
| Frontend | Render Static Site | React / Vite |
| Backend | Render Web Service | FastAPI |
| Database | Neon Cloud | PostgreSQL |
| MQTT Broker | Local Docker | Eclipse Mosquitto |
| MQTT Consumer | Local Docker | Python / Paho-MQTT |
| Cloud MQTT Consumer | Local Docker | Python / Paho-MQTT + Neon |
| Monitoring | Local Docker | Prometheus / Grafana |
| CI/CD | GitHub Actions + Render | Automated testing and deployment |

The existing local development environment remains available through Docker Compose.

### Data Flow

```text
Simulated Sensor Publisher
           |
           | MQTT
           v
    Eclipse Mosquitto
       (Local Docker)
           |
           v
    MQTT Cloud Consumer
       (Local Docker)
           |
           v
     Neon PostgreSQL
           |
           v
      FastAPI Backend
          (Render)
           |
           v
      React Frontend
          (Render)
```

The cloud consumer validates incoming measurements, applies threshold-based anomaly detection, and stores measurements and generated alerts in Neon PostgreSQL.

The FastAPI backend exposes the stored data through authenticated REST endpoints, which are consumed by the React frontend.

## 3. Why Render?

Render was selected as the application hosting platform for the following reasons:

- **Simplified Deployment:** Supports deployment directly from Git repositories.
- **Reduced Operational Overhead:** Eliminates the need to maintain a dedicated application server.
- **Environment Management:** Supports production configuration through environment variables.
- **Docker Compatibility:** Allows reuse of the existing backend container configuration.
- **Development Focus:** Enables faster progress without introducing unnecessary infrastructure complexity.

The frontend is deployed as a Render Static Site, while the backend runs as a Render Web Service.

## 4. Why Neon PostgreSQL?

Neon was selected as the managed PostgreSQL provider for cloud persistence.

- **PostgreSQL Compatibility:** Preserves the existing SQLAlchemy models, repositories, and database interactions.
- **Managed Infrastructure:** Eliminates the need to operate a dedicated cloud database server.
- **Cloud Accessibility:** Allows both the deployed FastAPI backend and the local cloud consumer to access the same database.
- **Minimal Application Changes:** Requires primarily database connection configuration rather than changes to the application architecture.

The local PostgreSQL container remains available for development and testing.

## 5. MQTT Deployment Decision

The initial deployment plan considered migrating the MQTT broker to EMQX Cloud and hosting the MQTT consumer as a cloud background worker.

However, the implemented Software V1 retains Eclipse Mosquitto and the MQTT consumers in the local Docker environment.

### Reasons for This Decision

- The existing Mosquitto infrastructure was already implemented and tested.
- MQTT authentication and topic-level ACLs were configured.
- The local consumer architecture was functioning reliably during integration testing.
- A separate cloud consumer could write measurements directly to Neon PostgreSQL.
- Managed MQTT hosting was not necessary to demonstrate the complete simulated sensor workflow.
- Keeping MQTT local reduced deployment complexity and additional infrastructure requirements.

### Deployment Limitation

The frontend and backend remain hosted on Render independently of the local Docker environment.

However, new MQTT measurements are ingested only while the local broker, cloud consumer, and a publisher are running.

This architecture does not provide continuously available cloud MQTT ingestion.

A managed MQTT broker such as EMQX Cloud remains a possible future option if remote connectivity or continuous ingestion becomes necessary.

## 6. Docker Configuration

Docker Compose is used to organize the local application infrastructure.

The deployment configuration is separated into three files:

| File | Purpose |
|---|---|
| `docker-compose.yml` | Local application stack |
| `docker-compose.cloud.yml` | MQTT cloud consumer connected to Neon |
| `docker-compose.monitoring.yml` | Prometheus and Grafana monitoring |

This separation allows the cloud ingestion and monitoring components to be managed independently of the main application stack.

The local Docker environment is also retained for development and integration testing.

## 7. CI/CD

GitHub Actions automates validation and deployment.

The workflow is triggered by pushes to the `futuristic-ui` branch and pull requests targeting the configured branches.

### Continuous Integration

- Backend automated tests using pytest
- Dedicated PostgreSQL test database
- Backend test coverage reporting
- Frontend dependency installation
- Frontend production build validation

### Continuous Deployment

After successful backend tests and frontend build validation, GitHub Actions triggers Render deployment hooks for:

- FastAPI Backend
- React Frontend

Deployment is triggered only for pushes to the `futuristic-ui` branch.

This ensures that automated deployment is initiated only after the CI jobs succeed.

## 8. Monitoring

Observability is implemented using Python logging, Prometheus, and Grafana.

The local MQTT consumer exposes an HTTP metrics endpoint on port `8001`.

Prometheus collects metrics every 15 seconds, and Grafana provides dashboards for monitoring MQTT ingestion and measurement processing.

Monitored metrics include:

- MQTT messages received
- MQTT messages rejected
- Measurements stored
- Anomalies detected
- Alerts created
- MQTT throughput
- Message rejection rate

Prometheus and Grafana remain local and are intended for administrator monitoring.

The production FastAPI application does not expose a public `/metrics` endpoint.

## 9. Future Physical Sensor Integration

The next integration stage will introduce an ESP32 microcontroller and a physical sensor.

The ESP32 will connect through Wi-Fi and publish measurements using MQTT.

The existing broker, consumer, database, API, and frontend architecture can be reused for local-network sensor integration.

Network accessibility, MQTT credentials, and payload compatibility will be configured and validated during hardware integration.

A managed cloud MQTT broker may be considered separately if sensors need to communicate from outside the local network.

## 10. Conclusion

AgroMonitor Software V1 has been deployed using a hybrid architecture combining Render, Neon PostgreSQL, and local Docker-based MQTT infrastructure.

The deployment provides:

- A hosted frontend and backend
- Managed PostgreSQL persistence
- MQTT-based simulated sensor ingestion
- Automated testing and deployment
- Local observability through Prometheus and Grafana
- Continued support for Docker-based development

The selected architecture meets the Software V1 objectives without introducing unnecessary infrastructure complexity.

Continuous cloud MQTT ingestion and managed MQTT hosting remain outside the current deployment scope.