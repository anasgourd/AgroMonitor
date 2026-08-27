NFR-01 — API Response Time
The system shall respond to standard API requests within 500 ms under normal operating conditions.

NFR-02 — Dashboard Load Time
The web application shall load the main field dashboard within 2 seconds under normal operating conditions.

NFR-03 — Horizontal Scalability
The backend architecture shall support horizontal scaling as the number of users, fields, sensors, and measurements increases.

NFR-05 — Fault Isolation
Failure or loss of communication with an individual sensor shall not prevent the system from receiving and processing data from other available sensors.

NFR-09 — System Observability
The system shall expose logs and metrics for application errors, data ingestion failures, processing failures, and ML pipeline failures, enabling the identification of the affected component and the time of failure.

NFR-10 — Authentication and Authorization
The system shall ensure that users can access only the fields, sensors, and data for which they are authorized.

NFR-15 — Platform Compatibility
The web application shall support the latest two stable versions of Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari on Windows, macOS, and Linux.