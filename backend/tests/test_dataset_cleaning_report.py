from pathlib import Path

from app.ml.dataset_cleaning_report import build_cleaning_report


def test_build_cleaning_report_tracks_defaults_and_standardization():
    raw_rows = [
        {
            "temp": "38.5",
            "cough": "productive cough",
            "shortness_of_breath": "medium",
            "throat_pain": "yes",
            "label": "influenza",
        }
    ]
    prepared_rows = [
        {
            "temperature": "38.5",
            "cough_type": "productive cough",
            "dyspnea_level": "medium",
            "sore_throat": "yes",
            "runny_nose": "",
            "headache_level": "",
            "muscle_pain": "",
            "fatigue_level": "",
            "duration_days": "",
            "oxygen_saturation": "",
            "heart_rate": "",
            "respiratory_rate": "",
            "chest_pain": "",
            "loss_of_taste": "",
            "diarrhea": "",
            "covid_contact": "",
            "smoker": "",
            "chronic_diseases": "",
            "diagnosis_label": "influenza",
        }
    ]
    normalized_rows = [
        {
            "temperature": "38.5",
            "cough_type": "wet",
            "dyspnea_level": "moderate",
            "sore_throat": "1",
            "runny_nose": "0",
            "headache_level": "none",
            "muscle_pain": "0",
            "fatigue_level": "0",
            "duration_days": "1",
            "oxygen_saturation": "98",
            "heart_rate": "80",
            "respiratory_rate": "18",
            "chest_pain": "0",
            "loss_of_taste": "0",
            "diarrhea": "0",
            "covid_contact": "0",
            "smoker": "0",
            "chronic_diseases": "",
            "diagnosis_label": "Gripp",
        }
    ]

    report = build_cleaning_report(
        source_path=Path("data/test.csv"),
        raw_rows=raw_rows,
        prepared_rows=prepared_rows,
        normalized_rows=normalized_rows,
    )

    assert report["rows_with_any_change"] == 1
    assert report["changed_field_counts"]["cough_type"] == 1
    assert report["changed_field_counts"]["diagnosis_label"] == 1
    assert report["defaulted_field_counts"]["oxygen_saturation"] == 1
    assert report["enum_standardizations"]["cough_type"] == 1
    assert report["label_standardizations"] == 1
