from app.ml.explainability_report import build_explainability_report
from app.ml.features import FEATURE_NAMES
from app.ml.statistical_model import train_naive_bayes


def test_build_explainability_report_returns_label_signals():
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
    report = build_explainability_report(artifact, top_n=3)

    assert report["label_count"] == 2
    assert report["global_top_signals"]
    assert report["per_label"]["A"]["top_feature_signals"]
    top_signal = report["per_label"]["B"]["top_feature_signals"][0]
    assert top_signal["feature"] in {"temperature_bin", "cough_type"}
    assert top_signal["support_score"] > 0
