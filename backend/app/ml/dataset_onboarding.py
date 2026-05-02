from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def load_mapping_template(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_dataset_headers(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)
        return next(reader, [])


def _resolve_source_column(field_config: dict[str, Any], headers: list[str]) -> tuple[str | None, str]:
    header_lookup = {header.strip().lower(): header for header in headers}
    explicit_source = field_config.get("source_column")
    if explicit_source:
        matched = header_lookup.get(str(explicit_source).strip().lower())
        if matched is not None:
            return matched, "explicit"
        return None, "missing_explicit"

    for alias in field_config.get("accepted_aliases", []):
        matched = header_lookup.get(str(alias).strip().lower())
        if matched is not None:
            return matched, "alias"

    return None, "missing"


def resolve_mapping_fields(headers: list[str], mapping: dict[str, Any]) -> list[dict[str, Any]]:
    resolved_fields: list[dict[str, Any]] = []
    for field_config in mapping.get("fields", []):
        source_column, status = _resolve_source_column(field_config, headers)
        resolved_fields.append(
            {
                "canonical_field": str(field_config["canonical_field"]),
                "required": bool(field_config.get("required", False)),
                "source_column": source_column,
                "status": status,
                "accepted_aliases": field_config.get("accepted_aliases", []),
            }
        )
    return resolved_fields


def apply_mapping_to_rows(rows: list[dict[str, str]], mapping: dict[str, Any]) -> list[dict[str, str]]:
    if not rows:
        return []

    headers = list(rows[0].keys())
    resolved_fields = resolve_mapping_fields(headers, mapping)
    missing_required_fields = [
        item["canonical_field"]
        for item in resolved_fields
        if item["required"] and item["source_column"] is None
    ]
    if missing_required_fields:
        raise ValueError(
            "Required fields are not mapped: " + ", ".join(missing_required_fields)
        )

    mapped_rows: list[dict[str, str]] = []
    for row in rows:
        mapped_row: dict[str, str] = {}
        for item in resolved_fields:
            source_column = item["source_column"]
            if source_column is None:
                continue
            mapped_row[item["canonical_field"]] = str(row.get(source_column, "")).strip()
        mapped_rows.append(mapped_row)
    return mapped_rows


def build_onboarding_validation_report(
    dataset_path: Path,
    mapping_path: Path,
) -> dict[str, Any]:
    headers = load_dataset_headers(dataset_path)
    mapping = load_mapping_template(mapping_path)

    mapped_fields = resolve_mapping_fields(headers, mapping)
    missing_required_fields: list[str] = []
    missing_optional_fields: list[str] = []
    invalid_explicit_fields: list[str] = []
    used_dataset_columns: set[str] = set()
    explicit_mappings = 0
    alias_mappings = 0

    for item in mapped_fields:
        source_column = item["source_column"]
        status = item["status"]
        required = item["required"]
        canonical_field = item["canonical_field"]
        if source_column is not None:
            used_dataset_columns.add(source_column)
            if status == "explicit":
                explicit_mappings += 1
            elif status == "alias":
                alias_mappings += 1
        elif status == "missing_explicit":
            invalid_explicit_fields.append(canonical_field)
            if required:
                missing_required_fields.append(canonical_field)
            else:
                missing_optional_fields.append(canonical_field)
        elif required:
            missing_required_fields.append(canonical_field)
        else:
            missing_optional_fields.append(canonical_field)

    unused_dataset_columns = [header for header in headers if header not in used_dataset_columns]
    ready_for_pipeline = len(missing_required_fields) == 0

    recommendations: list[str] = []
    if invalid_explicit_fields:
        recommendations.append(
            "Mapping JSON dagi ba'zi source_column qiymatlari dataset headerlarida topilmadi; explicit mappinglarni qayta tekshiring."
        )
    if missing_required_fields:
        recommendations.append(
            "Required canonical fields uchun source_column mappinglarini to'ldiring yoki dataset headerlarini aliaslarga moslang."
        )
    if unused_dataset_columns:
        recommendations.append(
            "Ishlatilmayotgan ustunlarni tekshirib chiqing: ba'zilarini canonical fieldlarga map qilish mumkin."
        )
    if not recommendations:
        recommendations.append("Dataset mapping bazaviy onboarding tekshiruvlaridan o'tdi.")

    return {
        "dataset_path": str(dataset_path),
        "mapping_path": str(mapping_path),
        "total_dataset_columns": len(headers),
        "dataset_columns": headers,
        "explicit_mappings": explicit_mappings,
        "alias_mappings": alias_mappings,
        "mapped_fields": mapped_fields,
        "invalid_explicit_fields": invalid_explicit_fields,
        "missing_required_fields": missing_required_fields,
        "missing_optional_fields": missing_optional_fields,
        "unused_dataset_columns": unused_dataset_columns,
        "ready_for_pipeline": ready_for_pipeline,
        "recommendations": recommendations,
    }


def onboarding_report_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Real Dataset Onboarding Validation",
        "",
        f"- Dataset path: `{report['dataset_path']}`",
        f"- Mapping path: `{report['mapping_path']}`",
        f"- Total dataset columns: `{report['total_dataset_columns']}`",
        f"- Explicit mappings: `{report['explicit_mappings']}`",
        f"- Alias mappings: `{report['alias_mappings']}`",
        f"- Ready for pipeline: `{report['ready_for_pipeline']}`",
        "",
        "## Invalid Explicit Fields",
    ]

    if report["invalid_explicit_fields"]:
        for field in report["invalid_explicit_fields"]:
            lines.append(f"- {field}")
    else:
        lines.append("- None")

    lines.extend([
        "",
        "## Missing Required Fields",
    ])

    if report["missing_required_fields"]:
        for field in report["missing_required_fields"]:
            lines.append(f"- {field}")
    else:
        lines.append("- None")

    lines.extend(["", "## Unused Dataset Columns"])
    if report["unused_dataset_columns"]:
        for field in report["unused_dataset_columns"]:
            lines.append(f"- {field}")
    else:
        lines.append("- None")

    lines.extend(["", "## Field Mapping Status"])
    for item in report["mapped_fields"]:
        lines.append(
            f"- {item['canonical_field']}: status={item['status']}, source_column={item['source_column']}"
        )

    lines.extend(["", "## Recommendations"])
    for item in report["recommendations"]:
        lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def save_onboarding_report_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")


def save_onboarding_report_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
