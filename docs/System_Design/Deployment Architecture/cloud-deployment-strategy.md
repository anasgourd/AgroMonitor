# AgroMonitor — Cloud Deployment Strategy

**Status:** Planned

## 1. Overview

AgroMonitor V1 currently runs in a local Docker Compose environment, consisting of a React frontend, FastAPI backend, PostgreSQL database, Eclipse Mosquitto broker, and a dedicated MQTT consumer.

The next phase focuses on deploying the application to the cloud and enabling connectivity with remote IoT sensors.

The selected approach is **Render for application hosting and EMQX Cloud for managed MQTT messaging**.

The goal is to establish an accessible, maintainable deployment while minimizing infrastructure management overhead and preserving the existing application architecture.

## 2. Deployment Architecture

| Component | Current Implementation | Planned Cloud Deployment |
|---|---|---|
| Frontend | React/Vite in Docker | Render Static Site |
| Backend | FastAPI Docker container | Render Web Service |
| Database | PostgreSQL Docker container | Managed PostgreSQL |
| MQTT Broker | Self-hosted Eclipse Mosquitto | EMQX Cloud |
| MQTT Consumer | Dedicated Docker container | Render Background Worker or equivalent |
| MQTT Clients | Paho-MQTT | Paho-MQTT with TLS |

The existing Docker Compose environment will remain available for local development and integration testing.

## 3. Why Render?

Render was selected as a managed application hosting platform for the following reasons:

- **Simplified Deployment:** Supports Docker-based applications and deployment directly from Git repositories.
- **Reduced Operational Overhead:** Eliminates the need to manually configure and maintain a Linux server.
- **Managed Services:** Provides application hosting, environment variable management, and managed PostgreSQL.
- **Existing Docker Compatibility:** Allows reuse of the current backend Dockerfile and containerized application structure.
- **Development Focus:** Enables faster progress toward physical sensor integration and ML engineering.

## 4. Why EMQX Cloud?

EMQX Cloud was selected as the planned managed MQTT broker.

- **Remote Connectivity:** Enables physical IoT sensors to communicate with the deployed system.
- **Secure Communication:** Supports MQTT over TLS, authentication, and access control.
- **Managed Infrastructure:** Reduces the need to maintain and secure a publicly accessible MQTT broker.
- **Scalability:** Provides infrastructure options for future increases in sensor connectivity and message volume.
- **Protocol Compatibility:** Allows continued use of the existing Paho-MQTT publisher and consumer implementations.

The migration from Mosquitto to EMQX Cloud is primarily motivated by deployment convenience, remote connectivity, and reduced operational overhead, rather than performance limitations of Mosquitto.

## 5. Alternative Considered — Docker Compose on a VPS

An alternative approach would be to deploy the existing Docker Compose stack on a cloud virtual private server (VPS).

This would allow the application to retain its current container architecture, including the self-hosted Mosquitto broker and PostgreSQL database.

**Advantages:**
- Greater control over infrastructure and networking.
- Direct reuse of the existing Docker Compose setup.
- Practical experience with Linux administration, reverse proxies, firewalls, and production container management.

**Trade-offs:**
- Additional server configuration and maintenance.
- Responsibility for TLS, security updates, backups, monitoring, and availability.
- More time spent on infrastructure operations rather than application development.

**Decision:** Render + EMQX Cloud is preferred for the current project phase because it reduces deployment complexity and allows development to progress more quickly toward ML and CPS integration.

A VPS deployment remains a possible future option for additional DevOps experience or different infrastructure requirements.

## 6. Expected Changes

The cloud migration primarily affects infrastructure and service configuration rather than application logic.

**Components that remain unchanged:**
- MQTT topic structure and JSON measurement payload.
- Paho-MQTT client library.
- Measurement validation and anomaly detection logic.
- Measurement and alert persistence workflow.
- Core publisher–broker–consumer architecture.
- Existing Docker-based local development environment.

**Required changes:**
- Configure cloud application services and database connectivity.
- Replace local Mosquitto connection settings with EMQX Cloud endpoints.
- Configure MQTT authentication and TLS.
- Manage production secrets and environment variables.
- Adapt frontend configuration for production hosting.
- Configure service health checks and deployment-specific operational settings.

## 7. Future Integration

After cloud deployment, AgroMonitor will integrate an **ESP32 with a physical sensor**, replacing or complementing the simulated Python publisher.

The final end-to-end workflow will be:

```text
ESP32 + Physical Sensor
          |
          | MQTT over TLS
          v
      EMQX Cloud
          |
          v
 MQTT Consumer (Cloud)
          |
          v
   MeasurementService
          |
          v
  Managed PostgreSQL
          |
          v
     FastAPI Backend
          |
          v
    React Dashboard
```

End-to-end testing will verify the complete flow from physical sensor measurements to database persistence, anomaly detection, alerts, and frontend visualization.

## 8. Conclusion

The planned migration to **Render + EMQX Cloud** provides a practical path from local development to a cloud-accessible IoT application.

The approach preserves the existing software architecture, reuses containerization work, and reduces infrastructure maintenance responsibilities.

This allows the project to prioritize physical sensor integration, end-to-end validation, and future ML engineering capabilities.

The final deployment configuration will be validated against service availability, pricing, and operational requirements before implementation.