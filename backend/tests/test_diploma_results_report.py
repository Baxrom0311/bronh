from app.ml.diploma_results_report import build_diploma_results_report


def test_build_diploma_results_report_collects_core_sections():
    report = build_diploma_results_report(
        profile={
            "total_rows": 35,
            "total_labels": 7,
            "label_distribution": {"A": 10, "B": 5},
            "missing_counts": {"x": 4, "y": 1},
        },
        quality={
            "duplicate_rows": 0,
            "duplicate_rate": 0.0,
            "class_balance_ratio": 2.0,
            "warnings": ["Dataset hajmi juda kichik, model umumlashuvi cheklanishi mumkin."],
            "recommendations": ["Real dataset qo'shib sample sonini oshiring."],
        },
        cleaning={
            "rows_with_any_change": 2,
            "row_change_rate": 0.1,
            "total_field_changes": 5,
            "defaulted_field_counts": {"chronic_diseases": 3},
            "recommendations": ["Normalization qoidalarini diplom matniga kiriting."],
        },
        metrics={
            "train_samples": 28,
            "test_samples": 7,
            "metrics": {"accuracy": 0.91},
        },
        evaluation={
            "overall_accuracy": 0.89,
            "mean_accuracy": 0.88,
            "folds": 5,
            "per_label_accuracy": {"A": 1.0, "B": 0.8},
        },
        explainability={
            "label_count": 2,
            "feature_count": 18,
            "global_top_signals": [
                {"label": "A", "feature": "runny_nose", "value": "yes", "support_score": 2.3, "lift_ratio": 4.1}
            ],
        },
    )

    assert report["dataset_summary"]["total_rows"] == 35
    assert report["performance_summary"]["holdout_accuracy"] == 0.91
    assert report["explainability_summary"]["label_count"] == 2
    assert report["limitations"]
    assert report["recommendations"]
