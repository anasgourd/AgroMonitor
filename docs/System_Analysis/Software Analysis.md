# Software Analysis

## 1. Purpose

This document summarizes the software analysis performed for AgroMonitor.

The analysis focuses on understanding the system's functionality, main domain concepts, responsibilities, and interactions before implementation.

---

## 2. Analysis Approach

AgroMonitor uses an **Object-Oriented Analysis (OOAD)** approach.

The main domain concepts identified are:

- User
- Field
- Sensor
- Measurement
- Alert

---

## 3. Use Case Analysis

Use Cases were used to describe the main system functionality and the interaction between the Farmer and the system.

The main use cases are:

- UC-01 — View Fields
- UC-02 — View Field Information
- UC-03 — Manage Field
- UC-04 — View Sensors
- UC-05 — View Sensor Information
- UC-06 — Manage Sensors
- UC-07 — View Measurements
- UC-08 — View Alerts
- UC-09 — Record Measurements
- UC-10 — Generate Alerts

Detailed specifications are documented in:

`docs/use_cases/use_case_specifications.md`

---

## 4. Static Analysis

A **BCE (Boundary-Control-Entity)** model was used to identify the main objects and their responsibilities.

- **Boundary** — interaction with the user or external input
- **Control** — coordinates system operations
- **Entity** — represents domain information

The BCE model is documented in:

`docs/domain/bce_domain_class_diagram.svg`

Implementation details such as databases, repositories, APIs, and message brokers are intentionally excluded from this model.

---

## 5. Dynamic Analysis

**Sequence Diagrams** were used to describe the interactions between actors, boundaries, controls, and entities for the main use cases.

The diagrams remain at the conceptual level and do not include implementation-specific details.

---

## 6. Analysis Result

The analysis established:

- The main system functionality through Use Cases
- The main domain concepts through the BCE model
- Object responsibilities
- The interactions between system objects through Sequence Diagrams
- The conceptual measurement → anomaly detection → alert flow

These results provide the basis for the **System Design** phase.

---

## 7. Analysis → Design

The analysis answers:

> **What does the system do and what are its main concepts and interactions?**

The following System Design phase will determine:

> **How will the system be implemented?**