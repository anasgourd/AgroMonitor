def test_login_sql_injection(client):
    payload = "' OR '1'='1"

    response = client.post(
        "/auth/login",
        json={
            "username": payload,
            "password": "test-password",
        },
    )

    assert response.status_code == 401
    assert "access_token" not in response.json()