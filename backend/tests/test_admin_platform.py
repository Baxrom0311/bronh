def _register_and_login(client, email: str, role: str) -> dict[str, str]:
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
    return response.json()


def test_admin_stats_and_users(client):
    admin_tokens = _register_and_login(client, "admin-platform@cdss.uz", "admin")
    doctor_tokens = _register_and_login(client, "doctor-platform@cdss.uz", "doctor")
    _register_and_login(client, "patient-platform@cdss.uz", "patient")

    patient_response = client.post(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {doctor_tokens['access_token']}"},
        json={
            "full_name": "Gulbahor Karimova",
            "date_of_birth": "1992-02-14",
            "gender": "female",
            "height_cm": 165,
            "weight_kg": 58,
            "chronic_diseases": [],
            "allergies": [],
            "smoking_status": False,
            "vaccination_status": {"covid": True},
            "emergency_contact": "+998901112233",
        },
    )
    patient_id = patient_response.json()["id"]

    symptom_response = client.post(
        "/api/v1/symptoms/",
        headers={"Authorization": f"Bearer {doctor_tokens['access_token']}"},
        json={
            "patient_id": patient_id,
            "temperature": 38.1,
            "cough_type": "dry",
            "dyspnea_level": "mild",
            "sore_throat": True,
            "runny_nose": True,
            "headache_level": "mild",
            "muscle_pain": False,
            "fatigue_level": 4,
            "duration_days": 3,
            "oxygen_saturation": 97,
            "heart_rate": 88,
            "respiratory_rate": 20,
            "chest_pain": False,
            "loss_of_taste": False,
            "diarrhea": False,
            "chronic_diseases": [],
            "covid_contact": False,
            "smoker": False,
            "notes": "Yengil respirator simptomlar",
        },
    )
    record_id = symptom_response.json()["id"]

    diagnosis_response = client.post(
        "/api/v1/diagnoses/",
        headers={"Authorization": f"Bearer {doctor_tokens['access_token']}"},
        json={"record_id": record_id},
    )
    diagnosis_id = diagnosis_response.json()["id"]

    confirm_response = client.post(
        f"/api/v1/diagnoses/{diagnosis_id}/confirm",
        headers={"Authorization": f"Bearer {doctor_tokens['access_token']}"},
        json={"doctor_notes": "Ambulator kuzatuv tavsiya qilindi"},
    )
    assert confirm_response.status_code == 200

    stats_response = client.get(
        "/api/v1/admin/stats",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert stats_response.status_code == 200
    stats = stats_response.json()
    assert stats["total_users"] == 3
    assert stats["total_patients"] == 1
    assert stats["total_symptom_records"] == 1
    assert stats["total_diagnoses"] == 1
    assert stats["confirmed_diagnoses"] == 1
    assert stats["users_by_role"]["admin"] == 1
    assert stats["users_by_role"]["doctor"] == 1
    assert stats["users_by_role"]["patient"] == 1

    users_response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert users_response.status_code == 200
    users = users_response.json()
    assert len(users) == 3
    assert {user["role"] for user in users} == {"admin", "doctor", "patient"}


def test_non_admin_cannot_access_admin_platform_endpoints(client):
    doctor_tokens = _register_and_login(client, "doctor-no-admin@cdss.uz", "doctor")

    stats_response = client.get(
        "/api/v1/admin/stats",
        headers={"Authorization": f"Bearer {doctor_tokens['access_token']}"},
    )
    assert stats_response.status_code == 403

    users_response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {doctor_tokens['access_token']}"},
    )
    assert users_response.status_code == 403
