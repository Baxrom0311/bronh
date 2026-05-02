from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def _smoothed_probability(count: int, total: int, vocab_size: int) -> float:
    return (count + 1) / (total + vocab_size + 1)


def build_explainability_report(
    artifact: dict[str, Any],
    top_n: int = 5,
) -> dict[str, Any]:
    labels: list[str] = artifact["labels"]
    label_counts: dict[str, int] = artifact["label_counts"]
    feature_names: list[str] = artifact["feature_names"]
    total_samples = sum(label_counts.values())

    per_label: dict[str, dict[str, Any]] = {}
    for label in labels:
        label_total = label_counts[label]
        other_total = total_samples - label_total
        signals: list[dict[str, Any]] = []

        for feature in feature_names:
            vocab = artifact["feature_vocab"][feature]
            vocab_size = len(vocab)
            label_values: dict[str, int] = artifact["feature_value_counts"][feature][label]

            for value, count in label_values.items():
                other_count = sum(
                    artifact["feature_value_counts"][feature][other_label].get(value, 0)
                    for other_label in labels
                    if other_label != label
                )
                label_probability = _smoothed_probability(count, label_total, vocab_size)
                other_probability = _smoothed_probability(other_count, other_total, vocab_size)
                support_score = round(math.log(label_probability) - math.log(other_probability), 3)
                lift_ratio = round(label_probability / other_probability, 3)
                signals.append(
                    {
                        "feature": feature,
                        "value": value,
                        "label_count": count,
                        "label_probability": round(label_probability, 3),
                        "other_probability": round(other_probability, 3),
                        "lift_ratio": lift_ratio,
                        "support_score": support_score,
                    }
                )

        signals.sort(
            key=lambda item: (item["support_score"], item["lift_ratio"], item["label_count"]),
            reverse=True,
        )
        per_label[label] = {
            "sample_count": label_total,
            "prior_probability": round(label_total / total_samples, 3) if total_samples else 0.0,
            "top_feature_signals": signals[:top_n],
        }

    global_signals: list[dict[str, Any]] = []
    for label, summary in per_label.items():
        for signal in summary["top_feature_signals"]:
            global_signals.append({"label": label, **signal})
    global_signals.sort(
        key=lambda item: (item["support_score"], item["lift_ratio"], item["label_count"]),
        reverse=True,
    )

    return {
        "model_type": artifact["model_type"],
        "model_version": artifact["version"],
        "sample_count": total_samples,
        "label_count": len(labels),
        "feature_count": len(feature_names),
        "top_n": top_n,
        "per_label": per_label,
        "global_top_signals": global_signals[:top_n],
    }


def explainability_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Respiratory NB Explainability",
        "",
        f"- Model type: {report['model_type']}",
        f"- Model version: {report['model_version']}",
        f"- Samples: {report['sample_count']}",
        f"- Labels: {report['label_count']}",
        f"- Features: {report['feature_count']}",
        "",
        "## Global Top Signals",
        "",
        "| Label | Feature | Value | Support score | Lift | Count |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]

    for signal in report["global_top_signals"]:
        lines.append(
            f"| {signal['label']} | {signal['feature']} | {signal['value']} | "
            f"{signal['support_score']} | {signal['lift_ratio']} | {signal['label_count']} |"
        )

    for label, summary in report["per_label"].items():
        lines.extend(
            [
                "",
                f"## {label}",
                "",
                f"- Sample count: {summary['sample_count']}",
                f"- Prior probability: {summary['prior_probability']}",
                "",
                "| Feature | Value | Support score | Lift | Count |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for signal in summary["top_feature_signals"]:
            lines.append(
                f"| {signal['feature']} | {signal['value']} | "
                f"{signal['support_score']} | {signal['lift_ratio']} | {signal['label_count']} |"
            )

    return "\n".join(lines) + "\n"


def save_explainability_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")


def save_explainability_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
