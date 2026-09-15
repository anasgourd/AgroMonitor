# Software Analysis

## 1. Purpose

This document summarizes the software analysis performed for AgroMonitor.

The analysis focuses on understanding the system's functionality, main domain concepts, responsibilities, and interactions before implementation.

---

## 2. Analysis Approach

AgroMonitor uses an **Object-Oriented Analysis (OOAD)** approach.

The system contains identifiable domain concepts such as **Fields, Sensors, Measurements, and Alerts**, which have their own responsibilities, relationships, and interactions.

This makes an object-oriented approach suitable for modelling both the **static structure** and the **dynamic behavior** of the system.

## 3. Coverage of Use Cases

The analysis models are derived from and support the defined **use cases**.

The sequence diagrams describe how the identified actors, boundary objects, controllers, and domain objects collaborate to realize the corresponding use cases.

The static models provide the structural view, while the sequence diagrams provide the behavioral view.


## 4. Analysis Without Implementation Details

The analysis models are intentionally kept at an **abstract level** and avoid implementation-specific decisions.

The BCE/domain models and sequence diagrams describe:

- the relevant system objects and concepts,
- their responsibilities,
- their relationships,
- and their interactions.

Implementation details such as specific frameworks, APIs, databases, repositories, deployment technologies, and infrastructure are left for the **Design phase**.

This separation keeps the analysis focused on **what the system does and what concepts are involved**, rather than how the system will be implemented.

## 5. Transition to Design

The remaining implementation and architectural decisions will be addressed in the **Design phase**.

The design will translate the analysis results into an implementable software structure, including:

- software components,
- frontend components,
- backend services and APIs,
- data persistence,
- system architecture,
- and infrastructure concerns.