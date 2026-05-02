from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from app.ml.dataset_pipeline import CANONICAL_COLUMNS, ENUM_MAPS

NUMERIC_RANGES: dict[str, tuple[float, float]] = {
    "temperature": (34.0, 42.5),
    "fatigue_level": (0.0, 10.0),
    "duration_days": (0.0, 60.0),
    "oxygen_saturation": (70.0, 100.0),
    "heart_rate": (30.0, 220.0),
    "respiratory_rate": (5.0, 60.0),
}

BOOLEAN_FIELDS = (
    "sore_throat",
    "runny_nose",
    "muscle_pain",
    "chest_pain",
    "loss_of_taste",
    "diarrhea",
    "covid_contact",
    "smoker",
)

CATEGORICAL_ALLOWED_VALUES = {
    "cough_type": set(ENUM_MAPS["cough_type"].values()),
    "dyspnea_level": set(ENUM_MAPS["dyspnea_level"].values()),
    "headache_level": set(ENUM_MAPS["headache_level"].values()),
}


def _missing_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    return {
        field: sum(1 for row in rows if row.get(field, "") == "")
        for field in CANONICAL_COLUMNS
    }


def _duplicate_rows(rows: list[dict[str, str]]) -> int:
    row_counter = Counter(
        tuple((field, row.get(field, "")) for field in CANONICAL_COLUMNS)
        for row in rows
    )
    return sum(count - 1 for count in row_counter.values() if count > 1)


def _out_of_range_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for field, (minimum, maximum) in NUMERIC_RANGES.items():
        invalid = 0
        for row in rows:
            value = row.get(field, "")
            if value == "":
                continue
            try:
                numeric_value = float(value)
            except ValueError:
                invalid += 1
                continue
            if numeric_value < minimum or numeric_value > maximum:
                invalid += 1
        counts[field] = invalid
    return counts


def _invalid_categorical_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for field, allowed_values in CATEGORICAL_ALLOWED_VALUES.items():
        counts[field] = sum(
            1
            for row in rows
            if row.get(field, "") and row.get(field, "") not in allowed_values
        )

    for field in BOOLEAN_FIELDS:
        counts[field] = sum(
            1
            for row in rows
            if row.get(field, "") and row.get(field, "") not in {"0", "1"}
        )
    return counts


def build_data_quality_report(rows: list[dict[str, str]], dataset_path: Path) -> dict[str, Any]:
    missing_counts = _missing_counts(rows)
    duplicate_rows = _duplicate_rows(rows)
    out_of_range_counts = _out_of_range_counts(rows)
    invalid_categorical_counts = _invalid_categorical_counts(rows)
    label_distribution = Counter(row.get("diagnosis_label", "") for row in rows if row.get("diagnosis_label", ""))

    label_counts = list(label_distribution.values())
    class_balance_ratio = round(max(label_counts) / min(label_counts), 3) if label_counts and min(label_counts) else None

    warnings: list[str] = []
    recommendations: list[str] = []

    if len(rows) < 100:
        warnings.append("Dataset hajmi juda kichik, model umumlashuvi cheklanishi mumkin.")
        recommendations.append("Real dataset qo'shib sample sonini oshiring.")

    if duplicate_rows:
        warnings.append(f"{duplicate_rows} ta takrorlangan qator aniqlandi.")
        recommendations.append("Deduplication bosqichini cleaning pipeline ga qo'shing.")

    fields_with_missing = [field for field, count in missing_counts.items() if count > 0]
    if fields_with_missing:
        warnings.append(f"Missing qiymatlar bor: {', '.join(fields_with_missing)}.")
        recommendations.append("Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.")

    fields_out_of_range = [field for field, count in out_of_range_counts.items() if count > 0]
    if fields_out_of_range:
        warnings.append(f"Clinical range dan tashqaridagi qiymatlar bor: {', '.join(fields_out_of_range)}.")
        recommendations.append("Outlier va out-of-range validatsiyasini import bosqichida majburiy qiling.")

    invalid_categorical_fields = [field for field, count in invalid_categorical_counts.items() if count > 0]
    if invalid_categorical_fields:
        warnings.append(f"Noto'g'ri kategorik qiymatlar bor: {', '.join(invalid_categorical_fields)}.")
        recommendations.append("Enum mapping va canonical normalization qoidalarini kengaytiring.")

    if class_balance_ratio is not None and class_balance_ratio > 3:
        warnings.append(f"Class imbalance yuqori: ratio={class_balance_ratio}.")
        recommendations.append("Train bosqichida class weights yoki resampling ishlating.")

    if not warnings:
        recommendations.append("Dataset quality bazaviy tekshiruvlardan muvaffaqiyatli o'tdi.")

    return {
        "dataset_path": str(dataset_path),
        "total_rows": len(rows),
        "duplicate_rows": duplicate_rows,
        "duplicate_rate": round(duplicate_rows / len(rows), 3) if rows else 0.0,
        "missing_counts": missing_counts,
        "out_of_range_counts": out_of_range_counts,
        "invalid_categorical_counts": invalid_categorical_counts,
        "label_distribution": dict(sorted(label_distribution.items())),
        "class_balance_ratio": class_balance_ratio,
        "warnings": warnings,
        "recommendations": recommendations,
    }


def quality_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Respiratory Dataset Quality Report",
        "",
        f"- Dataset path: `{report['dataset_path']}`",
        f"- Total rows: `{report['total_rows']}`",
        f"- Duplicate rows: `{report['duplicate_rows']}`",
        f"- Duplicate rate: `{report['duplicate_rate']}`",
        f"- Class balance ratio: `{report['class_balance_ratio']}`",
        "",
        "## Warnings",
    ]

    if report["warnings"]:
        for item in report["warnings"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No major quality warnings.")

    lines.extend(["", "## Recommendations"])
    for item in report["recommendations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Missing Counts"])
    for field, count in report["missing_counts"].items():
        lines.append(f"- {field}: {count}")

    lines.extend(["", "## Out Of Range Counts"])
    for field, count in report["out_of_range_counts"].items():
        lines.append(f"- {field}: {count}")

    return "\n".join(lines) + "\n"


def save_quality_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")


def save_quality_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
