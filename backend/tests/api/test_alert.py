from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

#GET /users/{user_id}/alerts tests
def test_get_user_alerts():
    response = client.get("/users/3/alerts")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for alert in data:
        assert "alert_id" in alert
        assert "measurement_id" in alert
        assert "message" in alert
        assert "timestamp" in alert


def test_get_user_alerts_empty():
    response = client.get("/users/2/alerts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_user_alerts_not_found():
    response = client.get("/users/999999/alerts")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_alerts_invalid_id():
    response = client.get("/users/abc/alerts")

    assert response.status_code == 422
    
# GET /users/{user_id}/alerts   
def test_get_field_alerts():
    response = client.get("/fields/3/alerts")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for alert in data:
        assert "alert_id" in alert
        assert "measurement_id" in alert
        assert "message" in alert
        assert "timestamp" in alert


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

# GET /alerts/{alert_id}

def test_get_alert():
    response = client.get("/alerts/1")

    assert response.status_code == 200

    data = response.json()

    assert data["alert_id"] == 1
    assert data["measurement_id"] == 1
    assert data["message"] == "Anomaly detected"
    assert "timestamp" in data


def test_get_alert_not_found():
    response = client.get("/alerts/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_get_alert_invalid_id():
    response = client.get("/alerts/abc")

    assert response.status_code == 422