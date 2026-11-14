NFR-01 — API Response Time
The system shall respond to standard API requests within 500 ms for at least 95% of requests (p95) under a normal operating load of up to 20 concurrent users (or 10 requests per second).

NFR-02 — Dashboard Load Time
The web application shall fully render the main field dashboard and become interactive within 2 seconds for at least 95% of user sessions (p95) under a normal operating load of up to 20 concurrent users.

NFR-03 — Horizontal Scalability
The backend architecture shall support horizontal scaling so that increasing active users or measurement volume by at least 3x does not degrade performance beyond the baselines defined in NFR-01 and NFR-02.

NFR-04 — Fault Isolation
The system shall isolate sensor connection failures, timeouts, and malformed telemetry payloads at the individual sensor stream level, ensuring that a failure affecting one sensor does not impede data ingestion or storage for any other active sensor.

NFR-05 — System Observability
The system shall provide sufficient observability to enable the detection and identification of application, data ingestion, processing, and ML pipeline failures within 15 minutes of occurrence.

NFR-06 — Authentication and Authorization
The system shall ensure that users can access only the fields, sensors, and data for which they are authorized.

NFR-07 — Platform Compatibility
The web application shall support the latest two stable versions of Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari.
