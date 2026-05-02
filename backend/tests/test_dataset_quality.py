from pathlib import Path

from app.ml.dataset_quality import build_data_quality_report


def test_build_data_quality_report_flags_duplicates_and_outliers():
    rows = [
        {
            "temperature": "39.5",
            "cough_type": "dry",
            "dyspnea_level": "mild",
            "sore_throat": "1",
            "runny_nose": "0",
            "headache_level": "mild",
            "muscle_pain": "0",
            "fatigue_level": "7",
            "duration_days": "4",
            "oxygen_saturation": "96",
            "heart_rate": "104",
            "respiratory_rate": "20",
            "chest_pain": "0",
            "loss_of_taste": "0",
            "diarrhea": "0",
            "covid_contact": "0",
            "smoker": "0",
            "chronic_diseases": "",
            "diagnosis_label": "Gripp",
        },
        {
            "temperature": "39.5",
            "cough_type": "dry",
            "dyspnea_level": "mild",
            "sore_throat": "1",
            "runny_nose": "0",
            "headache_level": "mild",
            "muscle_pain": "0",
            "fatigue_level": "7",
            "duration_days": "4",
            "oxygen_saturation": "96",
            "heart_rate": "104",
            "respiratory_rate": "20",
            "chest_pain": "0",
            "loss_of_taste": "0",
            "diarrhea": "0",
            "covid_contact": "0",
            "smoker": "0",
            "chronic_diseases": "",
            "diagnosis_label": "Gripp",
        },
        {
            "temperature": "45.0",
            "cough_type": "mystery",
            "dyspnea_level": "severe",
            "sore_throat": "2",
            "runny_nose": "0",
            "headache_level": "severe",
            "muscle_pain": "0",
            "fatigue_level": "12",
            "duration_days": "90",
            "oxygen_saturation": "65",
            "heart_rate": "250",
            "respiratory_rate": "3",
            "chest_pain": "1",
            "loss_of_taste": "0",
            "diarrhea": "0",
            "covid_contact": "0",
            "smoker": "0",
            "chronic_diseases": "",
            "diagnosis_label": "Shoshilinch yordam kerak",
        },
    ]

    report = build_data_quality_report(rows, Path("data/test.csv"))

    assert report["duplicate_rows"] == 1
    assert report["out_of_range_counts"]["temperature"] == 1
    assert report["invalid_categorical_counts"]["cough_type"] == 1
    assert report["invalid_categorical_counts"]["sore_throat"] == 1
    assert len(report["warnings"]) >= 3
