from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)



def test_get_field_alerts_empty():
    response = client.get("/fields/2/alerts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_field_alerts_not_found():
    response = client.get("/fields/999999/alerts")

    assert response.status_code == 404
    assert response.json()["detail"] == "Field not found"


def test_get_field_alerts_invalid_id():
    response = client.get("/fields/abc/alerts")

    assert response.status_code == 422

GET /alerts/{alert_id}


GET /alerts/{alert_id}

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
