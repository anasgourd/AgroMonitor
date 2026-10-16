from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# GET /fields/{field_id} — owner can retrieve their field
def test_get_field(authenticated_client):
    response = authenticated_client.get("/fields/2")

    assert response.status_code == 200

    data = response.json()

    assert data["field_id"] == 2
    assert data["user_id"] == 1
    assert "field_name" in data
    assert "type" in data
    assert "area" in data


# GET /fields/{field_id} — field does not exist
def test_get_field_not_found(authenticated_client):
    response = authenticated_client.get("/fields/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# GET /fields/{field_id} — invalid field ID format
def test_get_field_invalid_id(authenticated_client):
    response = authenticated_client.get("/fields/abc")

    assert response.status_code == 422


# GET /fields/{field_id} — authentication is required
def test_get_field_requires_authentication(client):
    response = client.get("/fields/2")

    assert response.status_code == 401


# GET /fields/{field_id} — user cannot access another user's field
def test_get_other_users_field(authenticated_client):
    response = authenticated_client.get("/fields/3")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"
    
# PUT /fields/{field_id} — owner can update their field
def test_update_field(authenticated_client):
    response = authenticated_client.put(
        "/fields/2",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["field_id"] == 2
    assert data["user_id"] == 1
    assert data["field_name"] == "Updated Field"
    assert data["type"] == "Updated Type"
    assert data["area"] == 20.5

# PUT /fields/{field_id} — field does not exist
def test_update_field_not_found(authenticated_client):
    response = authenticated_client.put(
        "/fields/999999",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"

# PUT /fields/{field_id} — invalid field ID format
def test_update_field_invalid_id(authenticated_client):
    response = authenticated_client.put(
        "/fields/abc",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5,
        },
    )

    assert response.status_code == 422


# PUT /fields/{field_id} — invalid request body
def test_update_field_invalid_body(authenticated_client):
    response = authenticated_client.put(
        "/fields/2",
        json={
            "field_name": "Updated Field",
        },
    )

    assert response.status_code == 422
    
# PUT /fields/{field_id} — authentication is required
def test_update_field_requires_authentication(client):
    response = client.put(
        "/fields/2",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5,
        },
    )

    assert response.status_code == 401


# PUT /fields/{field_id} — user cannot update another user's field
def test_update_other_users_field(authenticated_client):
    response = authenticated_client.put(
        "/fields/3",
        json={
            "field_name": "Hacked Field",
            "type": "Updated Type",
            "area": 20.5,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"



# DELETE /fields/{field_id} — owner can delete their field
def test_delete_field(authenticated_client):
    create_response = authenticated_client.post(
        "/users/me/fields",
        json={
            "field_name": "Delete Test Field",
            "type": "Test Type",
            "area": 10.5,
        },
    )

    assert create_response.status_code == 201

    field_id = create_response.json()["field_id"]

    response = authenticated_client.delete(f"/fields/{field_id}")

    assert response.status_code == 204


# DELETE /fields/{field_id} — field does not exist
def test_delete_field_not_found(authenticated_client):
    response = authenticated_client.delete("/fields/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# DELETE /fields/{field_id} — invalid field ID format
def test_delete_field_invalid_id(authenticated_client):
    response = authenticated_client.delete("/fields/abc")

    assert response.status_code == 422


# DELETE /fields/{field_id} — authentication is required
def test_delete_field_requires_authentication(client):
    response = client.delete("/fields/2")

    assert response.status_code == 401


# DELETE /fields/{field_id} — user cannot delete another user's field
def test_delete_other_users_field(authenticated_client):
    response = authenticated_client.delete("/fields/3")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# DELETE /fields/{field_id} — field with associated sensors cannot be deleted
def test_delete_field_with_sensors(authenticated_client):
    create_field_response = authenticated_client.post(
        "/users/me/fields",
        json={
            "field_name": "Field With Sensor",
            "type": "Test Type",
            "area": 10.5,
        },
    )

    assert create_field_response.status_code == 201
    field_id = create_field_response.json()["field_id"]

    create_sensor_response = authenticated_client.post(
        f"/fields/{field_id}/sensors",
        json={
            "sensor_name": "Test Sensor",
            "type": "Temperature",
            "status": "active",
        },
    )

    assert create_sensor_response.status_code == 201

    response = authenticated_client.delete(f"/fields/{field_id}")

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Cannot delete field because it has associated sensors"
    )
    
# GET /fields/{field_id}/sensors — authentication is required
def test_get_field_sensors_requires_authentication(client):
    response = client.get("/fields/2/sensors")

    assert response.status_code == 401


# GET /fields/{field_id}/sensors — user cannot access another user's field
def test_get_other_users_field_sensors(authenticated_client):
    response = authenticated_client.get("/fields/3/sensors")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"
    
    
# POST /fields/{field_id}/sensors — owner can create a sensor
def test_create_field_sensor(authenticated_client):
    response = authenticated_client.post(
        "/fields/2/sensors",
        json={
            "sensor_name": "New Test Sensor",
            "status": "active",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["field_id"] == 2
    assert data["sensor_name"] == "New Test Sensor"
    assert data["status"] == "active"
    assert "sensor_id" in data


# POST /fields/{field_id}/sensors — field does not exist
def test_create_sensor_field_not_found(authenticated_client):
    response = authenticated_client.post(
        "/fields/999999/sensors",
        json={
            "sensor_name": "New Test Sensor",
            "status": "active",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# POST /fields/{field_id}/sensors — invalid field ID format
def test_create_sensor_invalid_field_id(authenticated_client):
    response = authenticated_client.post(
        "/fields/abc/sensors",
        json={
            "sensor_name": "New Test Sensor",
            "status": "active",
        },
    )

    assert response.status_code == 422


# POST /fields/{field_id}/sensors — authentication is required
def test_create_sensor_requires_authentication(client):
    response = client.post(
        "/fields/2/sensors",
        json={
            "sensor_name": "New Test Sensor",
            "status": "active",
        },
    )

    assert response.status_code == 401


# POST /fields/{field_id}/sensors — user cannot add a sensor to another user's field
def test_create_sensor_for_other_users_field(authenticated_client):
    response = authenticated_client.post(
        "/fields/3/sensors",
        json={
            "sensor_name": "Unauthorized Sensor",
            "status": "active",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# POST /fields/{field_id}/sensors — invalid request body
def test_create_sensor_invalid_body(authenticated_client):
    response = authenticated_client.post(
        "/fields/2/sensors",
        json={
            "sensor_name": "New Test Sensor",
        },
    )

    assert response.status_code == 422