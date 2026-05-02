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


def test_full_cdss_flow(client):
    doctor_token = _register_and_login(client, "doctor@cdss.uz", "doctor")

    patient_response = client.post(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "full_name": "Ali Valiyev",
            "date_of_birth": "1998-05-10",
            "gender": "male",
            "height_cm": 178,
            "weight_kg": 74,
            "chronic_diseases": ["astma"],
            "allergies": [],
            "smoking_status": False,
            "vaccination_status": {"covid": True},
            "emergency_contact": "+998901234567",
        },
    )
    assert patient_response.status_code == 201
    patient_id = patient_response.json()["id"]

    symptom_response = client.post(
        "/api/v1/symptoms/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "patient_id": patient_id,
            "temperature": 38.9,
            "cough_type": "wet",
            "dyspnea_level": "moderate",
            "sore_throat": True,
            "runny_nose": False,
            "headache_level": "moderate",
            "muscle_pain": True,
            "fatigue_level": 8,
            "duration_days": 6,
            "oxygen_saturation": 92,
            "heart_rate": 116,
            "respiratory_rate": 28,
            "chest_pain": True,
            "loss_of_taste": False,
            "diarrhea": False,
            "chronic_diseases": ["astma"],
            "covid_contact": False,
            "smoker": False,
            "notes": "So'nggi 2 kun yomonlashgan",
        },
    )
    assert symptom_response.status_code == 201
    record_id = symptom_response.json()["id"]

    diagnosis_response = client.post(
        "/api/v1/diagnoses/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={"record_id": record_id},
    )
    assert diagnosis_response.status_code == 201
    data = diagnosis_response.json()
    assert data["predicted_condition"] in {
        "Zotiljam (pnevmoniya)",
        "Shoshilinch yordam kerak",
        "Astma xuruji",
    }
    assert data["risk_level"] in {"high", "critical"}
    assert len(data["top_predictions"]) == 3
    assert "rule_signals" in data["explanation"]
    assert data["explanation"]["engine_mode"] in {"rules-only", "hybrid-ready"}
    if data["explanation"]["engine_mode"] == "hybrid-ready":
        assert data["explanation"]["model_support"] is not None
