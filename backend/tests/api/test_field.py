from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# GET /fields/{field_id} — existing field
def test_get_field():
    response = client.get("/fields/3")

    assert response.status_code == 200

    data = response.json()

    assert data["field_id"] == 3
    assert "user_id" in data
    assert "field_name" in data
    assert "type" in data
    assert "area" in data


# GET /fields/{field_id} — field does not exist
def test_get_field_not_found():
    response = client.get("/fields/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# GET /fields/{field_id} — invalid path parameter
def test_get_field_invalid_id():
    response = client.get("/fields/abc")

    assert response.status_code == 422
    
    
# PUT /fields/{field_id} — existing field
def test_update_field():
    response = client.put(
        "/fields/2",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["field_id"] == 2
    assert data["user_id"] == 3
    assert data["field_name"] == "Updated Field"
    assert data["type"] == "Updated Type"
    assert data["area"] == 20.5
    

# PUT /fields/{field_id} — field does not exist
def test_update_field_not_found():
    response = client.put(
        "/fields/999999",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"

# PUT /fields/{field_id} — invalid path parameter
def test_update_field_invalid_id():
    response = client.put(
        "/fields/abc",
        json={
            "field_name": "Updated Field",
            "type": "Updated Type",
            "area": 20.5
        }
    )

    assert response.status_code == 422


# PUT /fields/{field_id} — invalid request body
def test_update_field_invalid_body():
    response = client.put(
        "/fields/1",
        json={
            "field_name": "Updated Field"
        }
    )

    assert response.status_code == 422
    

# DELETE /fields/{field_id} — existing field
def test_delete_field():
    # Create a field first so the test does not depend on field_id=1
    create_response = client.post(
        "/users/1/fields",
        json={
            "field_name": "Delete Test Field",
            "type": "Test Type",
            "area": 10.5
        }
    )

    assert create_response.status_code == 201

    field_id = create_response.json()["field_id"]

    response = client.delete(f"/fields/{field_id}")

    assert response.status_code == 204


# DELETE /fields/{field_id} — field does not exist
def test_delete_field_not_found():
    response = client.delete("/fields/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


# DELETE /fields/{field_id} — invalid path parameter
def test_delete_field_invalid_id():
    response = client.delete("/fields/abc")

    assert response.status_code == 422