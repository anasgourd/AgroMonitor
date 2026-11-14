from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
    
#GET  /measurements/{measurement_id}
def test_get_measurement_unauthenticated(client):
    response = client.get("/measurements/1")

    assert response.status_code == 401

def test_get_measurement_not_owned(authenticated_client):
    # Measurement 1 belongs to user 3, while authenticated_client is user 1.
    response = authenticated_client.get("/measurements/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Measurement not found"

def test_get_measurement_not_found(authenticated_client):
    response = authenticated_client.get("/measurements/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Measurement not found"

def test_get_measurement_invalid_id(authenticated_client):
    response = authenticated_client.get("/measurements/abc")

    assert response.status_code == 422
