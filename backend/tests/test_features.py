from app.ml.features import build_feature_vector_from_mapping
from app.models.symptom_record import CoughType, DyspneaLevel, HeadacheLevel


def test_build_feature_vector_handles_enum_members():
    vector = build_feature_vector_from_mapping(
        {
            "temperature": 38.7,
            "cough_type": CoughType.wet,
            "dyspnea_level": DyspneaLevel.moderate,
            "headache_level": HeadacheLevel.severe,
            "sore_throat": True,
            "runny_nose": False,
            "muscle_pain": True,
            "fatigue_level": 8,
            "duration_days": 6,
            "oxygen_saturation": 92,
            "heart_rate": 112,
            "respiratory_rate": 26,
            "chest_pain": True,
            "loss_of_taste": False,
            "diarrhea": False,
            "covid_contact": False,
            "smoker": False,
            "chronic_diseases": ["astma"],
        }
    )

    assert vector["cough_type"] == "wet"
    assert vector["dyspnea_level"] == "moderate"
    assert vector["headache_level"] == "severe"
