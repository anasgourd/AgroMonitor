
import os
from pathlib import Path
from datetime import datetime

import pytest
from dotenv import load_dotenv
from sqlalchemy import URL, text
from fastapi.testclient import TestClient

from app.core.security import hash_password

# Load the project's root .env.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Tests must use a dedicated database.
password = os.getenv("POSTGRES_PASSWORD")

if not password:
    raise RuntimeError(
        "POSTGRES_PASSWORD is missing. "
        "Cannot configure the test database safely."
    )

test_database_url = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password=password,
    host="localhost",
    port=5433,
    database="agromonitor_test",
)

os.environ["DATABASE_URL"] = test_database_url.render_as_string(
    hide_password=False
)

# Import database-dependent modules only after configuring DATABASE_URL.
from app.core.base import Base
from app.core.database import engine, SessionLocal, get_db
from app.models.user import User
from app.models.field import Field
from app.models.sensor import Sensor
from app.models.measurement import Measurement
from app.models.alert import Alert
from app.main import app

print(f"\n[TEST DATABASE] {engine.url.database}")

if engine.url.database != "agromonitor_test":
    raise RuntimeError(
        f"Tests must use agromonitor_test, not {engine.url.database!r}"
    )


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def reset_test_data(create_test_schema):
    # Delete data in foreign-key-safe order.
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())

    with SessionLocal() as db:
        test_password_hash = hash_password("test-password")       
        # Users: IDs 1,2, 3, 5.
        db.add_all([
            User(
                user_id=1,
                username="test_user_1",
                full_name="Test User 1",
                password=test_password_hash,
            ),
            User(
                user_id=2,
                username="test_user_2",
                full_name="Test User 2",
                password=test_password_hash,
            ),
            User(
                user_id=3,
                username="tasos",
                full_name="Anastasis",
                password=test_password_hash,
            ),
            User(
                user_id=5,
                username="test_user_5",
                full_name="Test User 5",
                password=test_password_hash,
            ),
        ])
        db.flush()

        # Fields: IDs 2,3, 5, 6.
        db.add_all([
            Field(
                field_id=2,
                user_id=1,
                field_name="Test Field 2",
                type="Olive Grove",
                area=10.5,
            ),
            Field(
                field_id=3,
                user_id=3,
                field_name="mpeis",
                type="oranges",
                area=100,
            ),
            Field(
                field_id=6,
                user_id=1,
                field_name="Test Field",
                type="Olive Grove",
                area=10.5,
            ),
            Field(
                field_id=5,
                user_id=5,
                field_name="evanthia",
                type="olive",
                area=15,
            ),
            
        ])
        db.flush()

        # Sensor ID 1 belongs to field ID 3.
        db.add(
            Sensor(
                sensor_id=1,
                field_id=3,
                sensor_name="western_sensor",
                status="active",
            )
        )
        db.flush()

        # Measurement ID 1.
        db.add(
            Measurement(
                measurement_id=1,
                sensor_id=1,
                value=24.5,
                timestamp=datetime(2026, 9, 22, 16, 53, 1, 995419),
                unit="°C",
                is_anomalous=False,
            )
        )
        
        db.add(
            Measurement(
                measurement_id=7,
                sensor_id=1,
                value=24.5,
                timestamp=datetime(2026, 9, 22, 16, 53, 1, 995419),
                unit="°C",
                is_anomalous=True,
            )
        )
        db.flush()

        # Alert ID 1 belongs to measurement ID 1.
        db.add(
            Alert(
                alert_id=1,
                measurement_id=7,
                message="Anomaly detected",
                timestamp=datetime(2026, 9, 22, 17, 20, 6, 453950),
            )
        )

        db.commit()

        # Advance PostgreSQL sequences beyond the manually assigned IDs.
        sequence_columns = [
            ("users", "user_id"),
            ("fields", "field_id"),
            ("sensors", "sensor_id"),
            ("measurements", "measurement_id"),
            ("alerts", "alert_id"),
        ]

        for table_name, column_name in sequence_columns:
            db.execute(
                text(
                    f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table_name}', '{column_name}'),
                        (SELECT MAX({column_name}) FROM {table_name}),
                        true
                    )
                    """
                )
            )

        db.commit()


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


# Authenticated test client for user ID 1.

@pytest.fixture
def authenticated_client(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "test_user_1",
            "password": "test-password",
        },
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]
    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )

    return client

# Authenticated test client for user ID 2.
# Used to test authorization between different users.
@pytest.fixture
def second_user_client(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "test_user_2",
            "password": "test-password",
        },
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]
    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )

    return client



@pytest.fixture
def test_user(db_session):
    user = User(
        username="pytest_user",
        full_name="Pytest User",
        password=hash_password("test-password"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_field(db_session, test_user):
    field = Field(
        user_id=test_user.user_id,
        field_name="Pytest Field",
        type="Greenhouse",
        area=100.0,
    )
    db_session.add(field)
    db_session.commit()
    db_session.refresh(field)
    return field


@pytest.fixture
def test_sensor(db_session, test_field):
    sensor = Sensor(
        field_id=test_field.field_id,
        sensor_name="Pytest Temperature Sensor",
        status="active",
    )
    db_session.add(sensor)
    db_session.commit()
    db_session.refresh(sensor)
    return sensor
