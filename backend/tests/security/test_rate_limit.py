from fastapi.testclient import TestClient

from app.main import app
from app.core.rate_limit import limiter

client = TestClient(app)


def test_login_rate_limit():
    # Reset counters before testing
    limiter._storage.reset()

    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={
            "username": "invalid_user",
            "password": "wrong_password",
        },
        )

        assert response.status_code != 429

    # Sixth request should be blocked
    response = client.post(
        "/auth/login",
        json={
            "username": "invalid_user",
            "password": "wrong_password",
        },
    )

    assert response.status_code == 429