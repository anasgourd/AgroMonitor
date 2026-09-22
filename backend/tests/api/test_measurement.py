from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

# GET /sensors/{sensor_id}/measurements
def test_get_sensor_measurements():
    response = client.get("/sensors/1/measurements")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for measurement in data:
        assert "measurement_id" in measurement
        assert measurement["sensor_id"] == 1
        assert "value" in measurement
        assert "timestamp" in measurement
        assert "unit" in measurement
        assert "is_anomalous" in measurement


def test_get_sensor_measurements_empty():
    response = client.get("/sensors/2/measurements")

    assert response.status_code == 200
    assert response.json() == []


def test_get_sensor_measurements_sensor_not_found():
    response = client.get("/sensors/999999/measurements")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_get_sensor_measurements_invalid_id():
    response = client.get("/sensors/abc/measurements")

    assert response.status_code == 422
    
#GET  /measurements/{measurement_id}
def test_get_measurement():
    response = client.get("/measurements/1")

    assert response.status_code == 200

    data = response.json()

    assert data["measurement_id"] == 1
    assert data["sensor_id"] == 1
    assert "value" in data
    assert "timestamp" in data
    assert "unit" in data
    assert "is_anomalous" in data


def test_get_measurement_not_found():
    response = client.get("/measurements/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Measurement not found"


def test_get_measurement_invalid_id():
    response = client.get("/measurements/abc")

    assert response.status_code == 422
    
#test for checking the measurmeent input
def test_record_measurement():
    response = client.post(
        "/measurements",
        json={
            "sensor_id": 1,
            "value": 26.5,
            "timestamp": "2026-09-22T17:00:00",
            "unit": "°C"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "measurement_id" in data
    assert data["sensor_id"] == 1
    assert data["value"] == 26.5
    assert data["unit"] == "°C"
    assert data["is_anomalous"] is False
    assert "timestamp" in data