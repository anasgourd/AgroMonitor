# AgroMonitor

AgroMonitor is a full-stack IoT application for monitoring agricultural sensor data.

The system provides user authentication, field and sensor management, and MQTT-based sensor data ingestion. Measurements are processed and stored in PostgreSQL, with automated anomaly detection and alert generation. A web dashboard enables users to manage their agricultural fields and sensors, visualize historical measurements, and monitor alerts.

## Features

- User authentication and authorization
- Field and sensor management
- MQTT-based sensor data ingestion
- Historical measurement visualization
- Anomaly detection and automated alerts
- RESTful API for data access and management
- Cloud deployment
- Automated testing and CI/CD
- Logging and monitoring

## Demo

The application is deployed on Render with a Neon PostgreSQL database.

**Live Demo:** [https://agromonitor-frontend.onrender.com/]

*Sensor data ingestion currently runs through a local MQTT infrastructure.*

## Documentation

Detailed technical documentation, including system architecture, design decisions, implementation, testing, and deployment, is available in the [`docs/`](docs/) directory.
