# REST Backend Implementation

## 1. Backend Layers

### FastAPI Router

The Router handles HTTP requests and responses.

Responsibilities:

* Define API endpoints.
* Receive request parameters.
* Validate API input using Pydantic schemas.
* Call the appropriate Service.
* Return the response to the frontend.

The Router does not directly access the database.

### Service

The Service layer contains application-level logic and coordinates operations between the API and data-access layers.

For simple CRUD operations, a Service may simply delegate the operation to a Repository. More complex operations can include business rules, validation, orchestration, or calls to other services.

Example:

```python
def get_sensors_by_field(field_id: int):
    return sensor_repository.get_by_field(field_id)
```

### Repository

The Repository handles data access and isolates the rest of the application from database-specific operations.

For example:

```python
def get_by_field(field_id: int):
    return db.query(Sensor).filter(
        Sensor.field_id == field_id
    ).all()
```

The Repository uses SQLAlchemy to communicate with the database.

Pagination and filtering parameters can be passed to the Repository when required.

**Database access:** The initial implementation uses synchronous SQLAlchemy sessions. An asynchronous SQLAlchemy stack may be introduced later if higher concurrency requirements justify it.

### SQLAlchemy Models

SQLAlchemy models represent the database tables as Python classes.

For example:

```python
class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(Integer, primary_key=True)
    sensor_name = Column(String)
    status = Column(String)
    field_id = Column(Integer, ForeignKey("fields.field_id"))
```

Similar SQLAlchemy models are used for:

* `User`
* `Field`
* `Sensor`
* `Measurement`
* `Alert`

### Pydantic Schemas

Pydantic schemas define the structure of API requests and responses.

For example:

```python
class SensorResponse(BaseModel):
    sensor_id: int
    sensor_name: str
    status: str
```

FastAPI uses these schemas for validation, serialization, and API documentation.

---

## 2. Error Handling

Application-level errors are handled by the Service layer, while HTTP-specific responses are handled by the Router.

For example:

* Field does not exist → `404 Not Found`
* Field exists but has no sensors → `200 OK` with an empty list
* Field exists and has sensors → `200 OK` with the sensor data

The Service determines whether the field exists by using the appropriate Repository lookup before retrieving its sensors.

This keeps application logic separate from HTTP representation.

---

## 3. Dependency Injection

FastAPI's dependency injection mechanism (`Depends`) is used to provide Services, Repositories, and database sessions to the API layer.

This keeps object creation separate from request handling and makes components easier to test.

The dependency injection mechanism is an implementation detail and is not shown in the main architecture diagram.
