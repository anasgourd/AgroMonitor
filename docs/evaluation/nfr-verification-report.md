# AgroMonitor V1 — Non-Functional Requirements Verification Report

## 1. Overview

This document summarizes the verification of the seven Non-Functional Requirements (NFRs) defined for AgroMonitor V1.

Verification was performed through performance testing, browser audits, automated API tests, integration tests, configuration reviews, architecture reviews, and manual functional checks.

The report distinguishes between requirements that were verified under their specified conditions and requirements for which only partial evidence is available.

## 2. Verification Summary

| ID | Requirement | Verification Method | Status |
|---|---|---|---|
| NFR-01 | API Performance | Grafana k6 Load Testing | **Verified** |
| NFR-02 | Dashboard Load Time | Chrome Lighthouse | Partially Verified |
| NFR-03 | Horizontal Scalability | Architecture and Configuration Review | Partially Verified |
| NFR-04 | Fault Isolation | Unit Tests, Integration Tests, Code Review | Partially Verified |
| NFR-05 | System Observability | Configuration Review, Prometheus Functional Check | Partially Verified |
| NFR-06 | Authentication and Authorization | Automated API and Authorization Tests | Verified — Tested Scope |
| NFR-07 | Platform Compatibility | Manual Browser Testing | Partially Verified |

---

## 3. NFR-01 — API Performance

### Requirement

The system shall maintain an API response time of **500 milliseconds or less at the 95th percentile (p95)** under a workload of up to **20 concurrent users OR 10 requests per second**.

### Verification Method

Performance testing was conducted using **Grafana k6** against the deployed AgroMonitor backend hosted on Render.

The final load test used a constant arrival rate of 10 requests per second, with a 10-second warm-up period followed by 60 seconds of steady-state testing.

The test script is located at:

`backend/tests/performance/load_test.js`

### Test Configuration

| Parameter | Value |
|---|---|
| Testing tool | Grafana k6 |
| Target | Deployed Render backend |
| Workload | 10 requests/second |
| Warm-up | 10 seconds |
| Steady-state duration | 60 seconds |
| Required p95 | ≤ 500 ms |

### Results

| Metric | Result |
|---|---|
| HTTP requests | 601 |
| Successful responses | 601/601 |
| HTTP errors | 0 |
| Dropped iterations | 0 |
| p95 response time | **78.41 ms** |
| Required p95 threshold | 500 ms |
| Threshold result | **PASS** |

### Conclusion

**Status: VERIFIED — PASS**

The final k6 load test demonstrated that the deployed AgroMonitor API satisfies the specified performance requirement at **10 requests per second**.

The measured p95 response time was **78.41 ms**, significantly below the required 500 ms threshold. All 601 requests completed successfully, with no HTTP errors or dropped iterations.

Because NFR-01 explicitly defines the workload condition as **20 concurrent users OR 10 requests per second**, successful verification of the 10 requests/second scenario is sufficient to satisfy the requirement.

The verified performance claim applies to the tested API workload and deployment configuration.

---

## 4. NFR-02 — Dashboard Load Time

### Requirement

The system shall render a fully interactive field dashboard within **2 seconds at the 95th percentile**, under a workload of 20 concurrent users.

### Verification Method

Performance was evaluated using Google Chrome Lighthouse against the deployed AgroMonitor frontend.

Two Lighthouse audits were performed.

### Results

| Metric | First Run | Second Run |
|---|---:|---:|
| Performance Score | 90 | 99 |
| First Contentful Paint | 0.5 s | 0.5 s |
| Largest Contentful Paint | 0.6 s | 0.5 s |
| Total Blocking Time | 40 ms | 50 ms |
| Cumulative Layout Shift | 0 | 0 |
| Speed Index | 8.2 s | 1.3 s |

The second audit achieved a Lighthouse Performance Score of 99, with an LCP of 0.5 seconds and a Speed Index of 1.3 seconds.

### Limitations

Lighthouse does not directly establish the p95 time required for a fully interactive field dashboard under 20 concurrent users.

The measured LCP and Speed Index values are useful indicators of frontend performance but are not equivalent to the complete NFR-02 acceptance criterion.

### Conclusion

**Status: PARTIALLY VERIFIED**

The Lighthouse results provide positive evidence of frontend rendering performance.

However, the complete requirement has not been verified because dashboard interactivity at p95 under 20 concurrent users was not measured.

---

## 5. NFR-03 — Horizontal Scalability

### Requirement

The system shall support horizontal scaling to accommodate **three times the active users or measurement volume** without violating the performance limits established by NFR-01 and NFR-02.

### Verification Method

An architecture and configuration review was performed.

The review covered the FastAPI backend, SQLAlchemy database connections, JWT authentication, rate limiting, Docker Compose deployment, and MQTT ingestion architecture.

### Findings

**Backend architecture**

The FastAPI backend is organized into modular API routers, services, and repositories.

The API uses stateless JWT authentication, which supports multiple backend instances when they share the appropriate configuration and signing secret.

**Database**

The backend uses SQLAlchemy connection pooling with a configured pool size of 20 and no overflow.

Multiple backend instances can share PostgreSQL, but total database connection usage must be considered when scaling.

**Rate limiting**

The existing SlowAPI configuration uses in-memory rate-limit storage.

This means rate-limit counters are not automatically shared between multiple backend instances.

**Docker deployment**

The current local Docker Compose configuration exposes the backend through a fixed host port.

Horizontal scaling would require appropriate service routing and load balancing rather than simply starting multiple containers with the same host-port binding.

**MQTT ingestion**

The MQTT consumer processes incoming messages synchronously.

Running multiple standard subscribers on the same topic could result in duplicate processing rather than automatic workload distribution.

Scaling MQTT ingestion would require an appropriate distribution strategy and duplicate-handling mechanisms.

### Limitations

No experimental threefold scaling test was performed.

Therefore, the ability to maintain the NFR-01 and NFR-02 performance limits under three times the workload has not been demonstrated.

### Conclusion

**Status: PARTIALLY VERIFIED**

The architecture provides a foundation for horizontal scaling, particularly through modular backend components and stateless authentication.

However, distributed rate limiting, database connection management, load balancing, and MQTT workload distribution require additional consideration.

Full compliance with the threefold scalability requirement remains unverified.

---

## 6. NFR-04 — Fault Isolation

### Requirement

The system shall isolate sensor connection failures, timeouts, and malformed telemetry payloads at the individual sensor stream level, ensuring that a failure affecting one sensor does not impede data ingestion or storage for any other active sensor.

### Verification Method

Verification was performed through MQTT consumer unit tests, integration tests, and code review.

Additional tests were implemented to verify that failures associated with one sensor do not prevent subsequent messages from other sensors from being processed.

### Existing Test Coverage

The MQTT consumer tests cover:

- Malformed JSON payload rejection.
- Invalid telemetry schema rejection.
- Invalid UTF-8 payload rejection.
- Oversized payload rejection.
- Missing or inactive sensor handling.
- Future timestamp rejection.
- SQLAlchemy exception handling.
- Database session cleanup.
- MQTT connection and disconnection callbacks.
- MQTT reconnection configuration.

Integration tests additionally verify successful measurement persistence, anomaly detection, alert creation, and transaction rollback when alert creation fails.

### Additional Fault Isolation Tests

Two additional tests were implemented and passed.

**Test 1 — Malformed Payload Isolation**

`test_malformed_payload_does_not_block_other_sensor`

A malformed telemetry message is submitted for Sensor 1, followed by a valid message for Sensor 2.

The test verifies that the malformed payload is rejected and the valid measurement reaches the measurement service.

**Result: PASS**

**Test 2 — Sensor Processing Failure Isolation**

`test_sensor_database_failure_does_not_block_other_sensor`

A simulated SQLAlchemy exception is raised while processing a measurement from Sensor 1.

A subsequent measurement from Sensor 2 is then processed successfully by the mocked service.

The test also verifies database session cleanup.

**Result: PASS**

### Limitations

These tests demonstrate sequential recovery from handled failures.

They do not establish complete isolation against blocking database operations, sensor-specific timeouts, or concurrent sensor-processing failures.

The second test uses mocks rather than proving cross-sensor persistence through a real database.

### Conclusion

**Status: PARTIALLY VERIFIED**

Automated tests confirm that malformed telemetry and handled processing exceptions do not prevent subsequent valid sensor messages from being processed.

However, timeout isolation and complete cross-sensor failure independence remain unverified.

---

## 7. NFR-05 — System Observability

### Requirement

The system shall provide sufficient observability to enable the detection and identification of application, data ingestion, processing, and ML pipeline failures within **15 minutes of occurrence**.

### Verification Method

Verification was performed through code review, monitoring configuration review, and a functional Prometheus target check.

### Implemented Observability Components

**Application Logging**

The backend uses Python logging with timestamps, severity levels, module names, and log messages.

The MQTT consumer also records connection events, rejected messages, and handled processing errors.

**Prometheus Metrics**

The system defines counters for:

- MQTT messages received.
- MQTT messages rejected.
- Measurements stored.
- Anomalies detected.
- Alerts created.

The FastAPI application exposes a `/metrics` endpoint when metrics are enabled through configuration.

**Monitoring Infrastructure**

The project includes Docker Compose configurations for Prometheus and Grafana.

Prometheus is configured to scrape the Cloud Consumer metrics endpoint.

### Prometheus Configuration

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "agromonitor-cloud-consumer"
    metrics_path: /metrics
    static_configs:
      - targets:
          - "cloud-consumer:8001"
```

### Functional Verification

The Prometheus target:

`cloud-consumer:8001`

was confirmed to be **UP**.

This verifies successful metrics collection from the Cloud Consumer at the time of testing.

The configured scrape interval is 15 seconds.

### Limitations

The Prometheus alerts page showed that no alerting rules were configured.

Therefore, automatic failure detection within 15 minutes has not been demonstrated.

Additionally:

- FastAPI backend monitoring is not included in the reviewed scrape configuration.
- Complete application and processing failure monitoring has not been verified.
- ML pipeline failure monitoring has not been verified.
- Grafana alerting and notification delivery have not been demonstrated.

### Conclusion

**Status: PARTIALLY VERIFIED**

AgroMonitor provides application logging, Prometheus instrumentation, and a configured monitoring infrastructure.

Successful metrics collection from the Cloud Consumer was verified.

However, the requirement to detect and identify all specified failure categories within 15 minutes remains unverified.

---

## 8. NFR-06 — Authentication and Authorization

### Requirement

The system shall ensure that users can access only the fields, sensors, and data for which they are authorized.

### Verification Method

Verification was performed through automated FastAPI API tests covering JWT authentication, resource ownership, and unauthorized access attempts.

### Authentication

The application implements JWT-based authentication.

Tests verify that protected endpoints reject unauthenticated requests with HTTP 401.

### Authorization

Resource ownership is enforced through relationships between users, fields, sensors, and measurements.

The reviewed tests verify that users cannot access resources belonging to other users.

| Resource | Verified Authorization Scenarios |
|---|---|
| Users | Unauthorized profile access and modification rejected |
| Fields | Unauthorized read, update, and delete rejected |
| Sensors | Unauthorized read, update, and delete rejected |
| Measurements | Unauthorized direct read rejected |
| Sensor measurements | Unauthorized access to another user's sensor measurements rejected |
| Alerts | Unauthorized user-level and field-level access rejected |
| Sensor creation | Creating a sensor under another user's field rejected |

### BOLA / IDOR Protection

The tests specifically cover Broken Object Level Authorization (BOLA) scenarios.

Examples include:

- `test_get_other_users_field`
- `test_update_other_users_field`
- `test_delete_other_users_field`
- `test_get_sensor_not_owned`
- `test_update_sensor_not_owned`
- `test_delete_sensor_not_owned`
- `test_get_measurement_not_owned`
- `test_get_sensor_measurements_not_owned`
- `test_get_other_user_alerts_forbidden`

Unauthorized attempts to access resources owned by another user return HTTP 404 in the reviewed tests.

This prevents access to the requested resource and avoids directly disclosing its existence through the endpoint response.

### Conclusion

**Status: VERIFIED — TESTED SCOPE**

The reviewed automated tests confirm that authentication and resource ownership restrictions are enforced across the tested user, field, sensor, measurement, and alert endpoints.

No BOLA vulnerability was demonstrated in the tested scenarios.

This verification does not constitute a complete security audit of every possible endpoint or attack path.

---

## 9. NFR-07 — Platform Compatibility

### Requirement

The web application shall support the latest two stable versions of:

- Google Chrome.
- Mozilla Firefox.
- Microsoft Edge.
- Safari.

### Verification Method

Manual browser testing of the AgroMonitor frontend.

### Results

| Browser | Verification |
|---|---|
| Google Chrome | Tested |
| Microsoft Edge | Tested |
| Mozilla Firefox | Not tested |
| Safari | Not tested |
| Previous stable browser versions | Not tested |

The application was accessed successfully through Google Chrome and Microsoft Edge.

### Limitations

No cross-browser testing was performed on Firefox or Safari.

The previous stable versions of the supported browsers were also not tested.

The available manual checks do not establish complete functional compatibility across all required browser versions.

### Conclusion

**Status: PARTIALLY VERIFIED**

Basic browser compatibility was demonstrated on Chrome and Edge.

Full compliance with the latest-two-stable-versions requirement remains unverified.

---

## 10. Final Assessment

AgroMonitor V1 has undergone non-functional verification covering performance, frontend rendering, scalability, fault isolation, observability, authentication, authorization, and browser compatibility.

The strongest verification evidence is available for:

- **NFR-01:** The deployed API satisfied the specified p95 performance threshold under the 10 requests/second workload.
- **NFR-06:** Automated API tests demonstrated authentication and resource ownership enforcement across the tested endpoints.

The remaining requirements have partial verification evidence but were not demonstrated under every specified acceptance condition.

These limitations are documented rather than treated as successful verification results.

### Deferred Verification

The following activities remain outside the completed V1 verification scope:

1. Dashboard interactivity testing at p95 under 20 concurrent users.
2. Experimental threefold horizontal scalability testing.
3. Sensor-specific timeout and concurrent fault-isolation testing.
4. Automated monitoring and failure-detection verification within 15 minutes.
5. Complete compatibility testing across all required browser versions.

### Overall Conclusion

AgroMonitor V1 demonstrates a good level of compliance with the defined non-functional requirements and is considered sufficiently mature for its current V1 scope.

The system has demonstrated satisfactory API performance under the specified workload of 10 requests/second, along with implemented and tested authentication and authorization controls.

While some aspects may benefit from further validation and improvement, the overall results indicate that AgroMonitor V1 meets its primary quality and performance objectives to a satisfactory degree.

The report documents the verification performed, supporting results, and areas for future improvement.