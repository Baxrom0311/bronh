from app.ml.diploma_chapter_draft import build_diploma_chapter_draft


def test_build_diploma_chapter_draft_contains_main_sections():
    content = build_diploma_chapter_draft(
        {
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
                "warnings": ["Dataset hajmi kichik."],
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
    )

    assert "## 3.1. Tadqiqot ma'lumotlari tavsifi" in content
    assert "## 3.4. Model interpretatsiyasi va explainability" in content
    assert "## 3.6. Bob bo'yicha xulosa" in content
    assert "holdout accuracy 1.0" not in content.lower()
    assert "35" in content
