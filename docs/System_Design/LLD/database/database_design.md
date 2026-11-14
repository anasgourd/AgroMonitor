# AgroMonitor — Database Design

## 1. Relationships and Constraints

The database follows the following relationships:

```text
User 1:N Field
Field 1:N Sensor
Sensor 1:N Measurement
Measurement 1:0..1 Alert
```

### Alert → Measurement

An `Alert` is associated directly with the `Measurement` that caused it:

```text
Alert.measurement_id
    → Measurement.measurement_id
```

An alert conceptually originates from an anomalous measurement, which is already represented by `Measurement.is_anomalous`.

Therefore, `Alert` does not store a `field_id` directly.

This avoids:

* **Redundancy** — the field can already be derived through `Measurement → Sensor → Field`.
* **Data inconsistency** — storing `field_id` separately could cause the alert's field to differ from the field associated with its measurement.
* **Unnecessary duplication** — the relationship to the field can be obtained through the existing foreign-key relationships.

For example, alerts for a specific field can be retrieved through:

```sql
SELECT a.*
FROM alert a
JOIN measurement m ON a.measurement_id = m.measurement_id
JOIN sensor s ON m.sensor_id = s.sensor_id
JOIN field f ON s.field_id = f.field_id
WHERE f.user_id = :user_id
  AND f.field_id = :field_id;
```

This keeps the database normalized and makes `Measurement` the source of the alert relationship.

---

## 2. Delete Behavior

Dependent records are deleted using cascading foreign keys.

The dependency hierarchy is:

```text
User
 └── Field
      └── Sensor
           └── Measurement
                └── Alert
```

The corresponding foreign keys use `ON DELETE CASCADE`:

```text
Field.user_id
    FK → User.user_id
    ON DELETE CASCADE

Sensor.field_id
    FK → Field.field_id
    ON DELETE CASCADE

Measurement.sensor_id
    FK → Sensor.sensor_id
    ON DELETE CASCADE

Alert.measurement_id
    FK → Measurement.measurement_id
    ON DELETE CASCADE
```

This prevents orphan records. In particular, an `Alert` should not remain in the database after the `Measurement` from which it was generated has been deleted.

Soft delete is not used because there is no requirement for retaining historical records of deleted Fields or Sensors.

---

## 3. Integrity Constraints

The database enforces the following integrity rules:

* Primary keys uniquely identify records.
* Foreign keys maintain valid relationships between tables.
* Required fields are defined as `NOT NULL`.
* `Measurement.is_anomalous` is a boolean value.
* `Measurement.timestamp` and `Alert.timestamp` store event times.
* `Field.area` must be non-negative.
* A `Measurement` cannot reference a non-existent `Sensor`.
* An `Alert` cannot reference a non-existent `Measurement`.
* Cascading deletes prevent dependent records from becoming orphaned.

---

## 4. Indexing Notes

The target RDBMS is **PostgreSQL**, which does not automatically create an index on foreign key columns.

Since foreign keys are used extensively for joins (`Field → Sensor → Measurement → Alert`) and for alert-retrieval queries, the following columns should be explicitly indexed during implementation:

* `Field.user_id`
* `Sensor.field_id`
* `Measurement.sensor_id`
* `Alert.measurement_id`

A composite index on `Measurement(sensor_id, timestamp)` should also be considered, since a primary access pattern for measurements is retrieving recent readings for a given sensor within a time range.

Exact index definitions, SQLAlchemy models, migrations, and connection configuration are handled during implementation.

---

## 5. Schema Reference

Column definitions and data types for each entity are defined in `api_design.md` and reflected in the relational/ER diagrams.

This document focuses on:

* relational structure
* primary and foreign-key relationships
* integrity constraints
* delete behavior
* indexing considerations

Column-level implementation details are intentionally handled separately during database implementation.
