from app.ml.diploma_defense_pack import (
    build_diploma_defense_speech,
    build_diploma_presentation_outline,
)


def _sample_report() -> dict[str, object]:
    return {
        "dataset_summary": {
            "total_rows": 35,
            "total_labels": 7,
            "train_samples": 28,
            "test_samples": 7,
            "top_labels": [{"name": "ARVI", "value": 5}],
            "top_missing_fields": [{"name": "chronic_diseases", "value": 26}],
        },
        "quality_summary": {
            "duplicate_rows": 0,
            "class_balance_ratio": 1.0,
            "warnings": ["Dataset hajmi juda kichik, model umumlashuvi cheklanishi mumkin."],
        },
        "cleaning_summary": {
            "rows_with_any_change": 0,
            "total_field_changes": 0,
            "top_defaulted_fields": [{"name": "chronic_diseases", "value": 26}],
        },
        "performance_summary": {
            "holdout_accuracy": 1.0,
            "cv_accuracy": 0.943,
            "folds": 5,
            "best_labels": [{"name": "ARVI", "value": 1.0}],
        },
        "explainability_summary": {
            "label_count": 7,
            "feature_count": 18,
            "top_global_signals": [
                {
                    "label": "COVID-19",
                    "feature": "loss_of_taste",
                    "value": "yes",
                    "support_score": 2.95,
                    "lift_ratio": 19.2,
                }
            ],
        },
        "limitations": ["Seed dataset sintetik."],
        "recommendations": ["Real dataset bilan qayta tekshirish."],
    }


def test_build_diploma_defense_pack_contains_core_sections():
    report = _sample_report()

    outline = build_diploma_presentation_outline(report)
    speech = build_diploma_defense_speech(report)

    assert "## Slayd 7. Baholash natijalari" in outline
    assert "## Slayd 10. Xulosa va keyingi ishlar" in outline
    assert "holdout aniqligi 1.0" in speech.lower()
    assert "savollaringiz bo'lsa" in speech.lower()
