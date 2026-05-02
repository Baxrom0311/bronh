from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from app.ml.features import FEATURE_NAMES, build_feature_vector_from_mapping

NUMERIC_FIELDS = (
    "temperature",
    "fatigue_level",
    "duration_days",
    "oxygen_saturation",
    "heart_rate",
    "respiratory_rate",
)

CATEGORICAL_FIELDS = (
    "cough_type",
    "dyspnea_level",
    "headache_level",
    "diagnosis_label",
)


def load_raw_dataset(dataset_path: Path) -> list[dict[str, str]]:
    with dataset_path.open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def _numeric_summary(rows: list[dict[str, str]], field: str) -> dict[str, float | int | None]:
    values = [float(row[field]) for row in rows if row.get(field) not in {None, ""}]
    if not values:
        return {"count": 0, "min": None, "max": None, "mean": None}
    return {
        "count": len(values),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
        "mean": round(mean(values), 3),
    }


def _categorical_summary(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    counts = Counter(row.get(field, "") for row in rows if row.get(field, ""))
    return dict(sorted(counts.items()))


def _missing_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    missing: dict[str, int] = {}
    if not rows:
        return missing
    for field in rows[0]:
        missing[field] = sum(1 for row in rows if row.get(field, "") == "")
    return missing


def _feature_distribution(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    distributions: dict[str, Counter[str]] = {feature: Counter() for feature in FEATURE_NAMES}
    for row in rows:
        vector = build_feature_vector_from_mapping(row)
        for feature in FEATURE_NAMES:
            distributions[feature][vector[feature]] += 1
    return {
        feature: dict(sorted(counter.items()))
        for feature, counter in distributions.items()
    }


def build_dataset_profile(rows: list[dict[str, str]], dataset_path: Path) -> dict[str, Any]:
    label_distribution = _categorical_summary(rows, "diagnosis_label")
    return {
        "dataset_path": str(dataset_path),
        "total_rows": len(rows),
        "total_labels": len(label_distribution),
        "label_distribution": label_distribution,
        "missing_counts": _missing_counts(rows),
        "numeric_summary": {
            field: _numeric_summary(rows, field)
            for field in NUMERIC_FIELDS
        },
        "categorical_summary": {
            field: _categorical_summary(rows, field)
            for field in CATEGORICAL_FIELDS
        },
        "feature_distribution": _feature_distribution(rows),
    }


def profile_to_markdown(profile: dict[str, Any]) -> str:
    lines = [
        "# Respiratory Seed Dataset Profile",
        "",
        f"- Dataset path: `{profile['dataset_path']}`",
        f"- Total rows: `{profile['total_rows']}`",
        f"- Total labels: `{profile['total_labels']}`",
        "",
        "## Label Distribution",
    ]
    for label, count in profile["label_distribution"].items():
        lines.append(f"- {label}: {count}")

    lines.append("")
    lines.append("## Numeric Summary")
    for field, summary in profile["numeric_summary"].items():
        lines.append(
            f"- {field}: count={summary['count']}, min={summary['min']}, max={summary['max']}, mean={summary['mean']}"
        )

    lines.append("")
    lines.append("## Missing Counts")
    for field, count in profile["missing_counts"].items():
        lines.append(f"- {field}: {count}")

    return "\n".join(lines) + "\n"


def save_profile_json(profile_path: Path, profile: dict[str, Any]) -> None:
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(json.dumps(profile, indent=2, ensure_ascii=True), encoding="utf-8")


def save_profile_markdown(markdown_path: Path, content: str) -> None:
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(content, encoding="utf-8")
