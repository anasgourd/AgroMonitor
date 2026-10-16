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

# GET /users/{user_id} — authenticated user can access own profile
def test_get_user(authenticated_client):
    response = authenticated_client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert "username" in data
    assert "full_name" in data


# GET /users/{user_id} — unauthenticated request is rejected
def test_get_user_requires_authentication(client):
    response = client.get("/users/1")

    assert response.status_code == 401


# GET /users/{user_id} — cannot access another user's profile
def test_get_other_user_forbidden(authenticated_client):
    response = authenticated_client.get("/users/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# GET /users/{user_id} — nonexistent user
def test_get_user_not_found(authenticated_client):
    response = authenticated_client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_invalid_id(authenticated_client):
    response = authenticated_client.get("/users/abc")

    assert response.status_code == 422
    

# PUT /users/{user_id} — authenticated user can update own profile
def test_update_user(authenticated_client):
    response = authenticated_client.put(
        "/users/1",
        json={
            "username": "updateduser",
            "full_name": "Updated User",
            "password": "newpassword",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["username"] == "updateduser"
    assert data["full_name"] == "Updated User"


# PUT /users/{user_id} — cannot update another user's profile
def test_update_other_user_forbidden(authenticated_client):
    response = authenticated_client.put(
        "/users/2",
        json={
            "username": "hackeduser",
            "full_name": "Hacked User",
            "password": "newpassword",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_not_found(authenticated_client):
    response = authenticated_client.put(
        "/users/999999",
        json={
            "username": "updateduser",
            "full_name": "Updated User",
            "password": "newpassword",
        },
    )

    assert response.status_code == 404


def test_update_user_invalid_id(authenticated_client):
    response = authenticated_client.put(
        "/users/abc",
        json={
            "username": "updateduser",
            "full_name": "Updated User",
            "password": "newpassword",
        },
    )

    assert response.status_code == 422


def test_update_user_invalid_body(authenticated_client):
    response = authenticated_client.put(
        "/users/1",
        json={"username": "updateduser"},
    )

    assert response.status_code == 422


# DELETE /users/{user_id} — existing user
def test_delete_user(client):
    # Create a user specifically for this test.
    create_response = client.post(
        "/users/",
        json={
            "username": "delete_test_user",
            "full_name": "Delete Test User",
            "password": "testpassword",
        },
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["user_id"]

    # Authenticate as the user we just created.
    login_response = client.post(
        "/auth/login",
        json={
            "username": "delete_test_user",
            "password": "testpassword",
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})

    # A user can delete their own account.
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204


def test_delete_user_not_found(authenticated_client):
    response = authenticated_client.delete("/users/999999")
    assert response.status_code == 404


def test_delete_user_invalid_id(authenticated_client):
    response = authenticated_client.delete("/users/abc")
    assert response.status_code == 422

    

# GET /users/{user_id}/fields — authenticated user can access own fields
def test_get_user_fields(authenticated_client):
    response = authenticated_client.get("/users/1/fields")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    for field in data:
        assert field["user_id"] == 1
        assert "field_id" in field
        assert "field_name" in field
        assert "type" in field
        assert "area" in field


def test_get_user_fields_empty(authenticated_client):
    response = authenticated_client.get("/users/2/fields")

    # User 2 is not the authenticated user, so access is hidden.
    assert response.status_code == 404


def test_get_other_user_fields_forbidden(authenticated_client):
    response = authenticated_client.get("/users/3/fields")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_fields_requires_authentication(client):
    response = client.get("/users/1/fields")

    assert response.status_code == 401


def test_get_user_fields_not_found(authenticated_client):
    response = authenticated_client.get("/users/999999/fields")

    assert response.status_code == 404


def test_get_user_fields_invalid_id(authenticated_client):
    response = authenticated_client.get("/users/abc/fields")

    assert response.status_code == 422

# POST /users/me/fields — valid request
def test_create_field(authenticated_client):
    response = authenticated_client.post(
        "/users/me/fields",
        json={
            "field_name": "Test Field",
            "type": "Olive Grove",
            "area": 10.5,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert "field_id" in data
    assert data["user_id"] == 1
    assert data["field_name"] == "Test Field"
    assert data["type"] == "Olive Grove"
    assert data["area"] == 10.5




# POST /users/me/fields — created field belongs to the authenticated user
def test_create_field_belongs_to_authenticated_user(authenticated_client):
    response = authenticated_client.post(
        "/users/me/fields",
        json={
            "field_name": "Test Field",
            "type": "Olive Grove",
            "area": 10.5,
        },
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == 1


# POST /users/me/fields — unauthenticated request is rejected

def test_create_field_requires_authentication(client):
    response = client.post(
        "/users/me/fields",
        json={
            "field_name": "Test Field",
            "type": "Olive Grove",
            "area": 10.5,
        },
    )

    assert response.status_code == 401




# POST /users/me/fields — missing required fields are rejected
def test_create_field_invalid_body(authenticated_client):
    response = authenticated_client.post(
        "/users/me/fields",
        json={
            "field_name": "Test Field",
        },
    )

    assert response.status_code == 422



# GET /users/{user_id}/alerts 

def test_get_user_alerts(authenticated_client):
    # User 1 is authenticated. User 1 has no seeded alerts.
    response = authenticated_client.get("/users/1/alerts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_user_alerts_requires_authentication(client):
    response = client.get("/users/1/alerts")

    assert response.status_code == 401


def test_get_other_user_alerts_forbidden(authenticated_client):
    # User 3 owns the seeded alert, but the client is authenticated as user 1.
    response = authenticated_client.get("/users/3/alerts")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_alerts_not_found(authenticated_client):
    response = authenticated_client.get("/users/999999/alerts")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_alerts_invalid_id(authenticated_client):
    response = authenticated_client.get("/users/abc/alerts")

    assert response.status_code == 422
