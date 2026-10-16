
# GET /sensors/{sensor_id}


def create_owned_sensor(authenticated_client):
    """Create a sensor owned by the authenticated test user."""
    response = authenticated_client.post(
        "/users/me/fields",
        json={
            "field_name": "Sensor Test Field",
            "type": "Greenhouse",
            "area": 100
        }
    )

    assert response.status_code == 201, response.text
    field_id = response.json()["field_id"]

    response = authenticated_client.post(
        f"/fields/{field_id}/sensors",
        json={
            "sensor_name": "Test Temperature Sensor",
            "status": "active"
        }
    )

    assert response.status_code == 201, response.text
    return response.json()


def test_get_sensor(authenticated_client):
    sensor = create_owned_sensor(authenticated_client)

    response = authenticated_client.get(
        f"/sensors/{sensor['sensor_id']}"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["sensor_id"] == sensor["sensor_id"]
    assert data["field_id"] == sensor["field_id"]
    assert data["sensor_name"] == "Test Temperature Sensor"
    assert data["status"] == "active"


def test_get_sensor_unauthenticated(client):
    response = client.get("/sensors/1")

    assert response.status_code == 401


def test_get_sensor_not_owned(authenticated_client):
    # Sensor 1 belongs to a field owned by another user.
    response = authenticated_client.get("/sensors/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_get_sensor_not_found(authenticated_client):
    response = authenticated_client.get("/sensors/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_get_sensor_invalid_id(authenticated_client):
    response = authenticated_client.get("/sensors/abc")

    assert response.status_code == 422


# PUT /sensors/{sensor_id}


def test_update_sensor(authenticated_client):
    sensor = create_owned_sensor(authenticated_client)

    response = authenticated_client.put(
        f"/sensors/{sensor['sensor_id']}",
        json={
            "sensor_name": "Updated Temperature Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["sensor_id"] == sensor["sensor_id"]
    assert data["field_id"] == sensor["field_id"]
    assert data["sensor_name"] == "Updated Temperature Sensor"
    assert data["status"] == "inactive"


def test_update_sensor_unauthenticated(client):
    response = client.put(
        "/sensors/1",
        json={
            "sensor_name": "Updated Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 401


def test_update_sensor_not_owned(authenticated_client):
    response = authenticated_client.put(
        "/sensors/1",
        json={
            "sensor_name": "Unauthorized Update",
            "status": "inactive"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_update_sensor_not_found(authenticated_client):
    response = authenticated_client.put(
        "/sensors/999999",
        json={
            "sensor_name": "Updated Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_update_sensor_invalid_id(authenticated_client):
    response = authenticated_client.put(
        "/sensors/abc",
        json={
            "sensor_name": "Updated Sensor",
            "status": "inactive"
        }
    )

    assert response.status_code == 422


def test_update_sensor_invalid_body(authenticated_client):
    sensor = create_owned_sensor(authenticated_client)

    response = authenticated_client.put(
        f"/sensors/{sensor['sensor_id']}",
        json={"sensor_name": "Updated Sensor"}
    )

    assert response.status_code == 422


# DELETE /sensors/{sensor_id}


def test_delete_sensor(authenticated_client):
    sensor = create_owned_sensor(authenticated_client)

    response = authenticated_client.delete(
        f"/sensors/{sensor['sensor_id']}"
    )

    assert response.status_code == 204


def test_delete_sensor_unauthenticated(client):
    response = client.delete("/sensors/1")

    assert response.status_code == 401


def test_delete_sensor_not_owned(authenticated_client):
    response = authenticated_client.delete("/sensors/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_delete_sensor_not_found(authenticated_client):
    response = authenticated_client.delete("/sensors/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_delete_sensor_invalid_id(authenticated_client):
    response = authenticated_client.delete("/sensors/abc")

    assert response.status_code == 422


# GET /sensors/{sensor_id}/measurements


def test_get_sensor_measurements(authenticated_client):
    sensor = create_owned_sensor(authenticated_client)

    response = authenticated_client.get(
        f"/sensors/{sensor['sensor_id']}/measurements"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_sensor_measurements_unauthenticated(client):
    response = client.get("/sensors/1/measurements")

    assert response.status_code == 401


def test_get_sensor_measurements_not_owned(authenticated_client):
    response = authenticated_client.get("/sensors/1/measurements")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"


def test_get_sensor_measurements_not_found(authenticated_client):
    response = authenticated_client.get(
        "/sensors/999999/measurements"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found"
