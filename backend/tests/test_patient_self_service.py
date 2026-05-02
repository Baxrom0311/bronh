def _register_and_login(client, email: str, role: str = "patient") -> str:
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "Password123",
            "full_name": "Test Patient",
            "role": role,
            "preferred_language": "uz",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Password123"},
    )
    return login_response.json()["access_token"]


def _create_patient(client, token: str, full_name: str = "Test Patient") -> dict:
    response = client.post(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": full_name,
            "date_of_birth": "2001-01-01",
            "gender": "female",
            "height_cm": 165,
            "weight_kg": 58,
            "chronic_diseases": [],
            "allergies": [],
            "smoking_status": False,
            "vaccination_status": {"covid": True},
            "emergency_contact": "+998900000000",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_patient_role_can_create_own_profile(client):
    token = _register_and_login(client, "patient@example.com")

    patient = _create_patient(client, token)

    assert patient["full_name"] == "Test Patient"


def test_patient_role_can_list_and_open_only_own_profile(client):
    own_token = _register_and_login(client, "patient-own@example.com")
    other_token = _register_and_login(client, "patient-other@example.com")
    own_patient = _create_patient(client, own_token, "Own Patient")
    other_patient = _create_patient(client, other_token, "Other Patient")

    list_response = client.get(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {own_token}"},
    )
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [own_patient["id"]]

    own_get_response = client.get(
        f"/api/v1/patients/{own_patient['id']}",
        headers={"Authorization": f"Bearer {own_token}"},
    )
    assert own_get_response.status_code == 200

    other_get_response = client.get(
        f"/api/v1/patients/{other_patient['id']}",
        headers={"Authorization": f"Bearer {own_token}"},
    )
    assert other_get_response.status_code == 403


def test_doctor_can_list_all_patient_profiles(client):
    first_token = _register_and_login(client, "first-patient@example.com")
    second_token = _register_and_login(client, "second-patient@example.com")
    doctor_token = _register_and_login(client, "doctor@example.com", "doctor")
    _create_patient(client, first_token, "First Patient")
    _create_patient(client, second_token, "Second Patient")

    response = client.get(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {doctor_token}"},
    )

    assert response.status_code == 200
    assert {item["full_name"] for item in response.json()} == {"First Patient", "Second Patient"}
