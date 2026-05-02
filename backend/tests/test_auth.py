def test_register_and_login(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "doctor@example.com",
            "password": "Password123",
            "full_name": "Test Doctor",
            "role": "doctor",
            "preferred_language": "uz",
        },
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "doctor@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "doctor@example.com", "password": "Password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "refresh_token" in login_response.json()


def test_refresh_and_logout_flow(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "patient@example.com",
            "password": "Password123",
            "full_name": "Test Patient",
            "role": "patient",
            "preferred_language": "uz",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "patient@example.com", "password": "Password123"},
    )
    assert login_response.status_code == 200
    tokens = login_response.json()

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200

    refresh_as_access_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert refresh_as_access_response.status_code == 401

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_response.status_code == 200
    refreshed_tokens = refresh_response.json()
    assert "access_token" in refreshed_tokens
    assert "refresh_token" in refreshed_tokens
    assert refreshed_tokens["refresh_token"] != refresh_token

    old_refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert old_refresh_response.status_code == 401

    logout_response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refreshed_tokens["refresh_token"]},
    )
    assert logout_response.status_code == 200
    assert logout_response.json()["status"] == "ok"

    revoked_refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refreshed_tokens["refresh_token"]},
    )
    assert revoked_refresh_response.status_code == 401
