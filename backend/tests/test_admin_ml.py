def _register_and_login(client, email: str, role: str) -> str:
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "Password123",
            "full_name": role.title(),
            "role": role,
            "preferred_language": "uz",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Password123"},
    )
    return response.json()["access_token"]


def test_admin_can_access_ml_metadata_and_retrain(client):
    admin_token = _register_and_login(client, "admin@cdss.uz", "admin")

    metadata_response = client.get(
        "/api/v1/admin/ml/metadata",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert metadata_response.status_code == 200
    assert metadata_response.json()["status"] == "ok"

    retrain_response = client.post(
        "/api/v1/admin/ml/retrain",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert retrain_response.status_code == 200
    data = retrain_response.json()
    assert data["status"] == "ok"
    assert data["metadata"]["ml_model_ready"] is True


def test_non_admin_cannot_retrain_ml_pipeline(client):
    doctor_token = _register_and_login(client, "doctor-ml@cdss.uz", "doctor")

    response = client.post(
        "/api/v1/admin/ml/retrain",
        headers={"Authorization": f"Bearer {doctor_token}"},
    )
    assert response.status_code == 403
