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


def test_doctor_can_confirm_diagnosis(client):
    doctor_token = _register_and_login(client, "doctor-confirm@cdss.uz", "doctor")

    patient_response = client.post(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "full_name": "Aliya Rahimova",
            "date_of_birth": "2001-07-20",
            "gender": "female",
            "height_cm": 168,
            "weight_kg": 60,
            "chronic_diseases": [],
            "allergies": [],
            "smoking_status": False,
            "vaccination_status": {"covid": True},
            "emergency_contact": "+998909998877",
        },
    )
    patient_id = patient_response.json()["id"]

    symptom_response = client.post(
        "/api/v1/symptoms/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "patient_id": patient_id,
            "temperature": 39.2,
            "cough_type": "wet",
            "dyspnea_level": "moderate",
            "sore_throat": True,
            "runny_nose": False,
            "headache_level": "moderate",
            "muscle_pain": True,
            "fatigue_level": 7,
            "duration_days": 5,
            "oxygen_saturation": 93,
            "heart_rate": 110,
            "respiratory_rate": 26,
            "chest_pain": True,
            "loss_of_taste": False,
            "diarrhea": False,
            "chronic_diseases": [],
            "covid_contact": False,
            "smoker": False,
            "notes": "Yo'tal va nafas qisishi kuchaygan",
        },
    )
    record_id = symptom_response.json()["id"]

    diagnosis_response = client.post(
        "/api/v1/diagnoses/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={"record_id": record_id},
    )
    diagnosis_id = diagnosis_response.json()["id"]

    confirm_response = client.post(
        f"/api/v1/diagnoses/{diagnosis_id}/confirm",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "confirmed_condition": "Zotiljam (pnevmoniya)",
            "doctor_notes": "Rentgen va CBC tavsiya qilindi",
        },
    )
    assert confirm_response.status_code == 200
    data = confirm_response.json()
    assert data["is_confirmed"] is True
    assert data["confirmed_condition"] == "Zotiljam (pnevmoniya)"
    assert data["doctor_notes"] == "Rentgen va CBC tavsiya qilindi"
    assert data["confirmed_by_user_id"] is not None
    assert data["confirmed_at"] is not None


def test_patient_cannot_confirm_diagnosis(client):
    patient_token = _register_and_login(client, "patient-confirm@cdss.uz", "patient")
    doctor_token = _register_and_login(client, "doctor-maker@cdss.uz", "doctor")

    patient_response = client.post(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "full_name": "Sarvar Tursunov",
            "date_of_birth": "1995-01-10",
            "gender": "male",
            "height_cm": 172,
            "weight_kg": 70,
            "chronic_diseases": [],
            "allergies": [],
            "smoking_status": False,
            "vaccination_status": {"covid": True},
            "emergency_contact": "+998907771122",
        },
    )
    patient_id = patient_response.json()["id"]

    symptom_response = client.post(
        "/api/v1/symptoms/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "patient_id": patient_id,
            "temperature": 37.8,
            "cough_type": "dry",
            "dyspnea_level": "none",
            "sore_throat": True,
            "runny_nose": True,
            "headache_level": "mild",
            "muscle_pain": False,
            "fatigue_level": 3,
            "duration_days": 2,
            "oxygen_saturation": 98,
            "heart_rate": 82,
            "respiratory_rate": 18,
            "chest_pain": False,
            "loss_of_taste": False,
            "diarrhea": False,
            "chronic_diseases": [],
            "covid_contact": False,
            "smoker": False,
            "notes": "Yengil ARVI ko'rinishi",
        },
    )
    record_id = symptom_response.json()["id"]

    diagnosis_response = client.post(
        "/api/v1/diagnoses/",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={"record_id": record_id},
    )
    diagnosis_id = diagnosis_response.json()["id"]

    confirm_response = client.post(
        f"/api/v1/diagnoses/{diagnosis_id}/confirm",
        headers={"Authorization": f"Bearer {patient_token}"},
        json={"doctor_notes": "No permission"},
    )
    assert confirm_response.status_code == 403
