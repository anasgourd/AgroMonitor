from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

# POST /users/ — valid request
def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpassword"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "user_id" in data
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"

# POST /users/ — missing required fields
def test_create_user_invalid_body():
    response = client.post(
        "/users/",
        json={
            "username": "testuser"
            # full_name και password λείπουν
        }
    )

    assert response.status_code == 422

# GET /users/{user_id} — existing user
def test_get_user():
    response = client.get("/users/1")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert "username" in data
    assert "full_name" in data

# GET /users/{user_id} — user does not exist
def test_get_user_not_found():
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

# GET /users/{user_id} — invalid path parameter
def test_get_user_invalid_id():
    response = client.get("/users/abc")

    assert response.status_code == 422
    

# PUT /users/{user_id} — existing user
def test_update_user():
    response = client.put(
        "/users/1",
        json={
            "username": "updateduser",
            "full_name": "Updated User",
            "password": "newpassword"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["username"] == "updateduser"
    assert data["full_name"] == "Updated User"


# PUT /users/{user_id} — user does not exist
def test_update_user_not_found():
    response = client.put(
        "/users/999999",
        json={
            "username": "updateduser",
            "full_name": "Updated User",
            "password": "newpassword"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# PUT /users/{user_id} — invalid path parameter
def test_update_user_invalid_id():
    response = client.put(
        "/users/abc",
        json={
            "username": "updateduser",
            "full_name": "Updated User",
            "password": "newpassword"
        }
    )

    assert response.status_code == 422


# PUT /users/{user_id} — missing required fields
def test_update_user_invalid_body():
    response = client.put(
        "/users/1",
        json={
            "username": "updateduser"
        }
    )

    assert response.status_code == 422
    

# DELETE /users/{user_id} — existing user
def test_delete_user():
    # Create a user for the test only.later this will change
    create_response = client.post(
        "/users/",
        json={
            "username": "delete_test_user",
            "full_name": "Delete Test User",
            "password": "testpassword"
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204


# DELETE /users/{user_id} — user does not exist
def test_delete_user_not_found():
    response = client.delete("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# DELETE /users/{user_id} — invalid path parameter
def test_delete_user_invalid_id():
    response = client.delete("/users/abc")

    assert response.status_code == 422
    

# GET /users/{user_id}/fields — existing user
def test_get_user_fields():
    response = client.get("/users/1/fields")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for field in data:
        assert "field_id" in field
        assert field["user_id"] == 1
        assert "field_name" in field
        assert "type" in field
        assert "area" in field

def test_get_user_fields_empty():
    # user exist but no fields
    response = client.get("/users/2/fields")

    assert response.status_code == 200
    assert response.json() == []


# GET /users/{user_id}/fields — user does not exist
def test_get_user_fields_not_found():
    response = client.get("/users/999999/fields")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# GET /users/{user_id}/fields — invalid path parameter
def test_get_user_fields_invalid_id():
    response = client.get("/users/abc/fields")

    assert response.status_code == 422

# POST /users/{user_id}/fields — valid request
def test_create_field():
    response = client.post(
        "/users/1/fields",
        json={
            "field_name": "Test Field",
            "type": "Olive Grove",
            "area": 10.5
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "field_id" in data
    assert data["user_id"] == 1
    assert data["field_name"] == "Test Field"
    assert data["type"] == "Olive Grove"
    assert data["area"] == 10.5


# POST /users/{user_id}/fields — user does not exist
def test_create_field_user_not_found():
    response = client.post(
        "/users/999999/fields",
        json={
            "field_name": "Test Field",
            "type": "Olive Grove",
            "area": 10.5
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# POST /users/{user_id}/fields — invalid path parameter
def test_create_field_invalid_user_id():
    response = client.post(
        "/users/abc/fields",
        json={
            "field_name": "Test Field",
            "type": "Olive Grove",
            "area": 10.5
        }
    )

    assert response.status_code == 422


# POST /users/{user_id}/fields — missing required fields
def test_create_field_invalid_body():
    response = client.post(
        "/users/1/fields",
        json={
            "field_name": "Test Field"
        }
    )

    assert response.status_code == 422