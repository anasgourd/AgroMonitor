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