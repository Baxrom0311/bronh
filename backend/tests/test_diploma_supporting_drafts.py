from app.ml.diploma_supporting_drafts import (
    build_diploma_chapter_1_draft,
    build_diploma_chapter_2_draft,
    build_diploma_conclusion_draft,
    build_diploma_full_draft,
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


def test_build_diploma_supporting_drafts_cover_key_sections():
    report = _sample_report()

    chapter_1 = build_diploma_chapter_1_draft(report)
    chapter_2 = build_diploma_chapter_2_draft(report)
    conclusion = build_diploma_conclusion_draft(report)
    full = build_diploma_full_draft(chapter_1, chapter_2, "# 3-bob", conclusion)

    assert "## 1.2. Tadqiqot maqsadi va vazifalari" in chapter_1
    assert "35 ta yozuv" in chapter_1
    assert "## 2.4. Klinik qaror mantiqi va model qatlami" in chapter_2
    assert "holdout accuracy 1.0" not in chapter_2.lower()
    assert "cross-validation accuracy: 0.943" in conclusion
    assert "# Diplom Ish Drafti" in full
    assert "# Xulosa" in full
