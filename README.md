# AgroMonitor

AgroMonitor is a full-stack IoT application for monitoring agricultural sensor data.

The system collects sensor measurements through MQTT, processes and stores them in PostgreSQL, and provides a web dashboard for visualization and monitoring.

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