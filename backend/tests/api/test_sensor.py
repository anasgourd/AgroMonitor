from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# GET /fields/{field_id}/sensors

def test_get_field_sensors():
    response = client.get("/fields/3/sensors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for sensor in data:
        assert "sensor_id" in sensor
        assert sensor["field_id"] == 3
        assert "sensor_name" in sensor
        assert "status" in sensor
        

def test_get_field_sensors_empty():
    response = client.get("/fields/6/sensors")

    assert response.status_code == 200
    assert response.json() == []
    
def test_get_field_sensors_field_not_found():
    response = client.get("/fields/999999/sensors")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


def test_get_field_sensors_invalid_id():
    response = client.get("/fields/abc/sensors")

    assert response.status_code == 422
    
    
# POST /fields/{field_id}/sensors

def test_create_sensor():
    response = client.post(
        "/fields/3/sensors",
        json={
            "sensor_name": "Temperature Sensor",
            "status": "active"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "sensor_id" in data
    assert data["field_id"] == 3
    assert data["sensor_name"] == "Temperature Sensor"
    assert data["status"] == "active"
    
def test_create_sensor_field_not_found():
    response = client.post(
        "/fields/999999/sensors",
        json={
            "sensor_name": "Temperature Sensor",
            "status": "active"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"

def test_create_sensor_invalid_id():
    response = client.post(
        "/fields/abc/sensors",
        json={
            "sensor_name": "Temperature Sensor",
            "status": "active"
        }
    )

    assert response.status_code == 422


def test_create_sensor_invalid_body():
    response = client.post(
        "/fields/1/sensors",
        json={
            "sensor_name": "Temperature Sensor"
        }
    )

    assert response.status_code == 422
    

# GET /sensors/{sensor_id}

def test_get_sensor():
    response = client.get("/sensors/1")

    assert response.status_code == 200

    data = response.json()

    assert data["sensor_id"] == 1
    assert "field_id" in data
    assert "sensor_name" in data
    assert "status" in data


def test_get_sensor_not_found():
    response = client.get("/sensors/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_get_sensor_invalid_id():
    response = client.get("/sensors/abc")

    assert response.status_code == 422
    
    

def test_update_sensor():
    response = client.put(
        "/sensors/1",
        json={
            "sensor_name": "Updated Temperature Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sensor_id"] == 1
    assert data["field_id"] == 3
    assert data["sensor_name"] == "Updated Temperature Sensor"
    assert data["status"] == "inactive"


def test_update_sensor_not_found():
    response = client.put(
        "/sensors/999999",
        json={
            "sensor_name": "Updated Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_update_sensor_invalid_id():
    response = client.put(
        "/sensors/abc",
        json={
            "sensor_name": "Updated Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 422


def test_update_sensor_invalid_body():
    response = client.put(
        "/sensors/1",
        json={
            "sensor_name": "Updated Sensor"
        }
    )

    assert response.status_code == 422
    
# DELETE /sensor/{sensor_id} — existing sensor   
def test_delete_sensor():
    create_response = client.post(
        "/fields/3/sensors",
        json={
            "sensor_name": "Delete Test Sensor",
            "status": "active"
        }
    )

    assert create_response.status_code == 201

    sensor_id = create_response.json()["sensor_id"]

    response = client.delete(
        f"/sensors/{sensor_id}"
    )

    assert response.status_code == 204


def test_delete_sensor_not_found():
    response = client.delete("/sensors/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_delete_sensor_invalid_id():
    response = client.delete("/sensors/abc")

    assert response.status_code == 422