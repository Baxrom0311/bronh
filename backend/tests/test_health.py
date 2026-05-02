def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "engine_mode" in response.json()


def test_model_metadata(client):
    response = client.get("/api/v1/health/model-metadata")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "engine_mode" in data
    assert "metrics" in data
    assert "evaluation_report" in data
    assert "explainability_report" in data
    assert "diploma_report" in data
    assert "cleaning_report" in data
    assert "data_quality_report" in data
    assert "split_manifest" in data
    assert "dataset_profile" in data


def test_swagger_docs_available(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Respiratory CDSS API" in response.text


def test_openapi_schema_contains_docs_metadata(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Respiratory CDSS API"
    assert "Respiratory CDSS backend API" in data["info"]["description"]
    tag_names = {tag["name"] for tag in data["tags"]}
    assert {"auth", "patients", "symptoms", "diagnoses", "admin", "admin-ml", "health"} <= tag_names


def test_wildcard_cors_does_not_allow_credentials():
    from app.core.config import Settings

    settings = Settings(cors_origins="*")
    assert settings.cors_origins_list == ["*"]
    assert settings.cors_allow_credentials is False
