from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_alert_unauthenticated(client):
    response = client.get("/alerts/1")

    assert response.status_code == 401


def test_get_alert_not_owned(authenticated_client):
    # Alert 1 belongs to user 3, while authenticated_client is user 1.
    response = authenticated_client.get("/alerts/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_get_alert_not_found(authenticated_client):
    response = authenticated_client.get("/alerts/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_get_alert_invalid_id(authenticated_client):
    response = authenticated_client.get("/alerts/abc")

    assert response.status_code == 422
