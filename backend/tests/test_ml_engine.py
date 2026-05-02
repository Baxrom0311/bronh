from app.ml.model import cdss_engine


def test_model_artifact_is_loaded():
    assert cdss_engine.mode in {"rules-only", "hybrid-ready"}
