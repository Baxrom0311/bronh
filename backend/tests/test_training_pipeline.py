from app.ml.features import FEATURE_NAMES
from app.ml.statistical_model import (
    cross_validate_naive_bayes,
    explain_prediction,
    split_samples_by_ids,
    train_naive_bayes,
)


def test_split_samples_by_ids_respects_manifest_order():
    samples = [
        {"sample_id": "1", "label": "A"},
        {"sample_id": "2", "label": "B"},
        {"sample_id": "3", "label": "C"},
    ]

    train_samples, test_samples = split_samples_by_ids(samples, ["3", "1"], ["2"])

    assert [sample["sample_id"] for sample in train_samples] == ["3", "1"]
    assert [sample["sample_id"] for sample in test_samples] == ["2"]


def test_cross_validate_naive_bayes_returns_fold_metrics():
    def build_sample(sample_id: str, label: str, temperature_bin: str, cough_type: str) -> dict[str, str]:
        sample = {feature: "none" for feature in FEATURE_NAMES}
        sample["temperature_bin"] = temperature_bin
        sample["cough_type"] = cough_type
        sample["sample_id"] = sample_id
        sample["label"] = label
        return sample

    samples = [
        build_sample("1", "A", "normal", "dry"),
        build_sample("2", "A", "normal", "dry"),
        build_sample("3", "A", "normal", "dry"),
        build_sample("4", "B", "high", "wet"),
        build_sample("5", "B", "high", "wet"),
        build_sample("6", "B", "high", "wet"),
    ]

    report = cross_validate_naive_bayes(samples, folds=3, seed=7)

    assert report["folds"] == 3
    assert report["samples"] == 6
    assert len(report["fold_results"]) == 3
    assert report["overall_accuracy"] == 1.0
    assert report["confusion_matrix"]["A"]["A"] == 3
    assert report["confusion_matrix"]["B"]["B"] == 3


def test_cross_validate_naive_bayes_handles_tiny_dataset():
    samples = [
        {**{feature: "none" for feature in FEATURE_NAMES}, "sample_id": "1", "label": "A"},
        {**{feature: "none" for feature in FEATURE_NAMES}, "sample_id": "2", "label": "B"},
    ]

    report = cross_validate_naive_bayes(samples, folds=5, seed=42)

    assert report["folds"] >= 1
    assert report["samples"] == 2
    assert len(report["fold_results"]) >= 1


def test_explain_prediction_returns_ranked_feature_support():
    def build_sample(sample_id: str, label: str, temperature_bin: str, cough_type: str) -> dict[str, str]:
        sample = {feature: "none" for feature in FEATURE_NAMES}
        sample["temperature_bin"] = temperature_bin
        sample["cough_type"] = cough_type
        sample["sample_id"] = sample_id
        sample["label"] = label
        return sample

    samples = [
        build_sample("1", "A", "normal", "dry"),
        build_sample("2", "A", "normal", "dry"),
        build_sample("3", "B", "high", "wet"),
        build_sample("4", "B", "high", "wet"),
    ]

    artifact = train_naive_bayes(samples)
    explanation = explain_prediction(
        artifact,
        {
            **{feature: "none" for feature in FEATURE_NAMES},
            "temperature_bin": "high",
            "cough_type": "wet",
        },
    )

    assert explanation["predicted_label"] == "B"
    assert explanation["runner_up_label"] == "A"
    assert explanation["top_supporting_features"]
    assert explanation["top_supporting_features"][0]["feature"] in {"temperature_bin", "cough_type"}
