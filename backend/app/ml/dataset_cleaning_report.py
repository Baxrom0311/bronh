from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.ml.dataset_pipeline import BOOL_FALSE, BOOL_TRUE, CANONICAL_COLUMNS, DEFAULTS, ENUM_MAPS

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


def build_cleaning_report(
    source_path: Path,
    raw_rows: list[dict[str, str]],
    prepared_rows: list[dict[str, str]],
    normalized_rows: list[dict[str, str]],
    mapping_path: Path | None = None,
) -> dict[str, Any]:
    changed_field_counts = {field: 0 for field in CANONICAL_COLUMNS}
    defaulted_field_counts = {field: 0 for field in CANONICAL_COLUMNS}
    boolean_standardizations = {field: 0 for field in BOOLEAN_FIELDS}
    enum_standardizations = {field: 0 for field in ENUM_MAPS}
    label_standardizations = 0
    chronic_disease_standardizations = 0
    rows_with_any_change = 0
    sample_changes: list[dict[str, object]] = []

    for row_index, (prepared_row, normalized_row) in enumerate(
        zip(prepared_rows, normalized_rows, strict=False),
        start=1,
    ):
        row_changed = False
        for field in CANONICAL_COLUMNS:
            before = str(prepared_row.get(field, "") or "").strip()
            after = normalized_row.get(field, "")

            if before == "" and after == DEFAULTS[field]:
                defaulted_field_counts[field] += 1

            if before == after:
                continue

            changed_field_counts[field] += 1
            row_changed = True

            lowered_before = before.lower()
            if field in BOOLEAN_FIELDS and lowered_before not in {"0", "1"} | BOOL_TRUE | BOOL_FALSE:
                boolean_standardizations[field] += 1
            elif field in BOOLEAN_FIELDS and lowered_before not in {"0", "1"}:
                boolean_standardizations[field] += 1

            if field in ENUM_MAPS:
                enum_standardizations[field] += 1
            elif field == "diagnosis_label":
                label_standardizations += 1
            elif field == "chronic_diseases":
                chronic_disease_standardizations += 1

            if len(sample_changes) < 12:
                sample_changes.append(
                    {
                        "row_index": row_index,
                        "field": field,
                        "before": before or "<empty>",
                        "after": after,
                    }
                )

        if row_changed:
            rows_with_any_change += 1

    changed_field_counts = {
        field: count
        for field, count in changed_field_counts.items()
        if count > 0
    }
    defaulted_field_counts = {
        field: count
        for field, count in defaulted_field_counts.items()
        if count > 0
    }
    boolean_standardizations = {
        field: count
        for field, count in boolean_standardizations.items()
        if count > 0
    }
    enum_standardizations = {
        field: count
        for field, count in enum_standardizations.items()
        if count > 0
    }

    total_field_changes = sum(changed_field_counts.values())
    recommendations: list[str] = []
    if mapping_path is not None:
        recommendations.append("Explicit mapping fayli qo'llanildi; real dataset onboarding uchun shu mappingni versiyalab saqlang.")
    if defaulted_field_counts:
        recommendations.append("Default bilan to'ldirilgan ustunlarni tekshirib, real datasetda bu maydonlarni to'liqroq yig'ishga harakat qiling.")
    if enum_standardizations or boolean_standardizations or label_standardizations:
        recommendations.append("Normalization qoidalari ishladi; diplom matnida preprocessing qadamlarini alohida jadval bilan ko'rsating.")
    if not recommendations:
        recommendations.append("Cleaning bosqichida katta transformatsiya aniqlanmadi.")

    return {
        "source_path": str(source_path),
        "mapping_path": str(mapping_path) if mapping_path is not None else None,
        "raw_columns": list(raw_rows[0].keys()) if raw_rows else [],
        "total_rows": len(normalized_rows),
        "rows_with_any_change": rows_with_any_change,
        "row_change_rate": round(rows_with_any_change / len(normalized_rows), 3) if normalized_rows else 0.0,
        "total_field_changes": total_field_changes,
        "changed_field_counts": dict(sorted(changed_field_counts.items())),
        "defaulted_field_counts": dict(sorted(defaulted_field_counts.items())),
        "boolean_standardizations": dict(sorted(boolean_standardizations.items())),
        "enum_standardizations": dict(sorted(enum_standardizations.items())),
        "label_standardizations": label_standardizations,
        "chronic_disease_standardizations": chronic_disease_standardizations,
        "sample_changes": sample_changes,
        "recommendations": recommendations,
    }


def cleaning_report_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Respiratory Dataset Cleaning Report",
        "",
        f"- Source path: `{report['source_path']}`",
        f"- Mapping path: `{report['mapping_path']}`",
        f"- Total rows: `{report['total_rows']}`",
        f"- Rows with any change: `{report['rows_with_any_change']}`",
        f"- Row change rate: `{report['row_change_rate']}`",
        f"- Total field changes: `{report['total_field_changes']}`",
        "",
        "## Changed Field Counts",
    ]

    if report["changed_field_counts"]:
        for field, count in report["changed_field_counts"].items():
            lines.append(f"- {field}: {count}")
    else:
        lines.append("- None")

    lines.extend(["", "## Defaulted Field Counts"])
    if report["defaulted_field_counts"]:
        for field, count in report["defaulted_field_counts"].items():
            lines.append(f"- {field}: {count}")
    else:
        lines.append("- None")

    lines.extend(["", "## Recommendations"])
    for item in report["recommendations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Sample Changes"])
    if report["sample_changes"]:
        for item in report["sample_changes"]:
            lines.append(
                f"- row {item['row_index']} | {item['field']}: {item['before']} -> {item['after']}"
            )
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def save_cleaning_report_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")


def save_cleaning_report_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
