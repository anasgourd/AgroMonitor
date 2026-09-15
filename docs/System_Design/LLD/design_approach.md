# Low-Level Design

## Purpose

The Low-Level Design defines how the main parts of AgroMonitor will be structured internally before implementation.

Different parts of the system require different design approaches, so the LLD uses the approach that best fits each part.

## Design Approach

### Frontend — Component-Level Design

The frontend will use component-level design.

The UI will be divided into a hierarchy of smaller components, with higher-level components composing lower-level components.

The planned structure is:

```text
Pages / Main Views
        ↓
Feature-Level Components
        ↓
Reusable UI Components
        ↓
Basic UI Elements
```

For example, a field dashboard will be composed of smaller components responsible for presenting different parts of the field information.

---

### Backend — Object-Oriented Design

The backend will use Object-Oriented Design (OOD).

The main concepts of the AgroMonitor domain will be represented as entities, while their behaviour and application operations will be distributed among appropriate classes.

The main domain entities are:

* **User** — represents a system user.
* **Field** — represents an agricultural field.
* **Sensor** — represents a sensor associated with a field.
* **Measurement** — represents a measurement produced by a sensor.
* **Alert** — represents an alert generated from the monitoring process.

These entities represent the state and concepts of the domain. They are separated from infrastructure concerns such as HTTP requests and database access.

Other classes provide the operations around these entities. For example:

```text
Controller
    ↓
Service
    ↓
Domain Entities
    ↓
Repository
    ↓
Database
```

The exact classes, responsibilities, relationships, and interactions will be defined through the LLD class and sequence diagrams.

---

### Data Stream Processing — Functional/Data-Flow-Oriented Design

The sensor-data processing pipeline will use a functional and data-flow-oriented design approach.

The processing will be organized as a sequence of focused operations, where data moves through stages such as validation, anomaly analysis, persistence, and alert generation.

For example:

```text
Incoming Measurement
        ↓
Validation
        ↓
Anomaly Analysis
        ↓
Persistence
        ↓
Alert Generation
```

Each processing step has a specific responsibility rather than having one large function handle the entire pipeline.

---

## Overall Software Quality

Using these approaches together allows each part of AgroMonitor to be designed according to its nature rather than forcing one design style onto the entire system.

Through these principles, we aim to achieve **Separation of Concerns, Single Responsibility, and High Cohesion and Low Coupling**.

### Separation of Concerns

Different responsibilities should be handled by different components, classes, or functions.

For example, the Controller handles API requests, the Service handles application logic, and the Repository handles data access. This keeps each part focused on a specific aspect of the system.

### Single Responsibility

Each component, class, or function should have a clear and focused responsibility.

For example, validation logic should not also be responsible for anomaly detection. Keeping these responsibilities separate makes each part easier to understand, test, and modify independently.

### High Cohesion and Low Coupling

Related functionality should stay together, while unnecessary dependencies between components should be minimized.

For example, measurement-related operations should remain within the appropriate measurement-related components, while measurement processing logic should not depend directly on the database implementation. This makes the system easier to maintain and change.

Together, these choices aim to produce software that is **modular, understandable, testable, and ovreall maintainable, and reliable**.
