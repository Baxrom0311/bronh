from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _top_items(items: dict[str, float] | dict[str, int], top_n: int = 3) -> list[dict[str, Any]]:
    return [
        {"name": name, "value": value}
        for name, value in sorted(items.items(), key=lambda item: item[1], reverse=True)[:top_n]
    ]


def _collect_limitations(
    profile: dict[str, Any] | None,
    quality: dict[str, Any] | None,
    metrics: dict[str, Any] | None,
) -> list[str]:
    limitations: list[str] = []
    total_rows = profile.get("total_rows") if profile else None
    quality_warnings = quality.get("warnings", []) if quality else []

    has_dataset_size_warning = any("Dataset hajmi" in item for item in quality_warnings)
    if isinstance(total_rows, int) and total_rows < 100 and not has_dataset_size_warning:
        limitations.append("Dataset hajmi kichik, model umumlashuvi cheklangan bo'lishi mumkin.")

    if quality:
        limitations.extend(quality_warnings)

    holdout_accuracy = metrics.get("metrics", {}).get("accuracy") if metrics else None
    if holdout_accuracy is not None and holdout_accuracy == 1.0 and isinstance(total_rows, int) and total_rows < 100:
        limitations.append("Yuqori accuracy sintetik seed dataset bilan bog'liq bo'lishi mumkin; real datasetda qayta tekshirish zarur.")

    unique_limitations: list[str] = []
    for item in limitations:
        if item not in unique_limitations:
            unique_limitations.append(item)
    return unique_limitations


def _collect_recommendations(
    quality: dict[str, Any] | None,
    cleaning: dict[str, Any] | None,
) -> list[str]:
    recommendations: list[str] = [
        "Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.",
        "NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.",
        "Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.",
    ]
    if quality:
        recommendations.extend(quality.get("recommendations", []))
    if cleaning:
        recommendations.extend(cleaning.get("recommendations", []))

    unique_recommendations: list[str] = []
    for item in recommendations:
        if item not in unique_recommendations:
            unique_recommendations.append(item)
    return unique_recommendations


def build_diploma_results_report(
    profile: dict[str, Any] | None,
    quality: dict[str, Any] | None,
    cleaning: dict[str, Any] | None,
    metrics: dict[str, Any] | None,
    evaluation: dict[str, Any] | None,
    explainability: dict[str, Any] | None,
) -> dict[str, Any]:
    label_distribution = profile.get("label_distribution", {}) if profile else {}
    missing_counts = profile.get("missing_counts", {}) if profile else {}
    per_label_accuracy = evaluation.get("per_label_accuracy", {}) if evaluation else {}
    defaulted_field_counts = cleaning.get("defaulted_field_counts", {}) if cleaning else {}
    global_signals = explainability.get("global_top_signals", []) if explainability else []

    return {
        "report_type": "diploma_ml_results",
        "dataset_summary": {
            "total_rows": profile.get("total_rows") if profile else None,
            "total_labels": profile.get("total_labels") if profile else None,
            "train_samples": metrics.get("train_samples") if metrics else None,
            "test_samples": metrics.get("test_samples") if metrics else None,
            "top_labels": _top_items(label_distribution),
            "top_missing_fields": _top_items(missing_counts),
        },
        "quality_summary": {
            "duplicate_rows": quality.get("duplicate_rows") if quality else None,
            "duplicate_rate": quality.get("duplicate_rate") if quality else None,
            "class_balance_ratio": quality.get("class_balance_ratio") if quality else None,
            "warning_count": len(quality.get("warnings", [])) if quality else 0,
            "warnings": quality.get("warnings", []) if quality else [],
        },
        "cleaning_summary": {
            "rows_with_any_change": cleaning.get("rows_with_any_change") if cleaning else None,
            "row_change_rate": cleaning.get("row_change_rate") if cleaning else None,
            "total_field_changes": cleaning.get("total_field_changes") if cleaning else None,
            "top_defaulted_fields": _top_items(defaulted_field_counts),
        },
        "performance_summary": {
            "holdout_accuracy": metrics.get("metrics", {}).get("accuracy") if metrics else None,
            "cv_accuracy": evaluation.get("overall_accuracy") if evaluation else None,
            "cv_mean_accuracy": evaluation.get("mean_accuracy") if evaluation else None,
            "folds": evaluation.get("folds") if evaluation else None,
            "best_labels": _top_items(per_label_accuracy),
        },
        "explainability_summary": {
            "label_count": explainability.get("label_count") if explainability else None,
            "feature_count": explainability.get("feature_count") if explainability else None,
            "top_global_signals": global_signals[:5],
        },
        "limitations": _collect_limitations(profile, quality, metrics),
        "recommendations": _collect_recommendations(quality, cleaning),
    }


def diploma_results_to_markdown(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    quality = report["quality_summary"]
    cleaning = report["cleaning_summary"]
    performance = report["performance_summary"]
    explainability = report["explainability_summary"]

    lines = [
        "# Diplom Uchun ML Natijalari",
        "",
        "## Qisqa Xulosa",
        "",
        f"- Dataset rows: `{dataset['total_rows']}`",
        f"- Labels: `{dataset['total_labels']}`",
        f"- Train/Test: `{dataset['train_samples']}` / `{dataset['test_samples']}`",
        f"- Holdout accuracy: `{performance['holdout_accuracy']}`",
        f"- CV accuracy: `{performance['cv_accuracy']}`",
        "",
        "## Dataset Holati",
        "",
        f"- Duplicate rows: `{quality['duplicate_rows']}`",
        f"- Class balance ratio: `{quality['class_balance_ratio']}`",
        f"- Rows with cleaning changes: `{cleaning['rows_with_any_change']}`",
        f"- Total field changes: `{cleaning['total_field_changes']}`",
        "",
        "### Eng ko'p uchragan label'lar",
    ]

    for item in dataset["top_labels"]:
        lines.append(f"- {item['name']}: {item['value']}")

    lines.extend(["", "### Eng ko'p missing bo'lgan maydonlar"])
    for item in dataset["top_missing_fields"]:
        lines.append(f"- {item['name']}: {item['value']}")

    lines.extend(["", "## Model Baholash", ""])
    lines.append(f"- Folds: `{performance['folds']}`")
    lines.append(f"- CV mean accuracy: `{performance['cv_mean_accuracy']}`")
    lines.append("- Eng yaxshi per-label accuracy natijalari:")
    for item in performance["best_labels"]:
        lines.append(f"- {item['name']}: {item['value']}")

    lines.extend(["", "## Explainability Highlights", ""])
    for signal in explainability["top_global_signals"]:
        lines.append(
            f"- {signal['label']}: {signal['feature']} = {signal['value']} | "
            f"support={signal['support_score']} | lift={signal['lift_ratio']}"
        )

    lines.extend(["", "## Limitations", ""])
    for item in report["limitations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Tavsiyalar", ""])
    for item in report["recommendations"]:
        lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def save_diploma_results_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")


def save_diploma_results_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
