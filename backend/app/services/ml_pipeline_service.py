from __future__ import annotations

import csv
import json
from pathlib import Path

from app.core.config import settings
from app.ml.explainability_report import (
    build_explainability_report,
    explainability_to_markdown,
    save_explainability_json,
    save_explainability_markdown,
)
from app.ml.diploma_results_report import (
    build_diploma_results_report,
    diploma_results_to_markdown,
    save_diploma_results_json,
    save_diploma_results_markdown,
)
from app.ml.diploma_chapter_draft import (
    build_diploma_chapter_draft,
    save_diploma_chapter_draft,
)
from app.ml.diploma_supporting_drafts import (
    build_diploma_chapter_1_draft,
    build_diploma_chapter_2_draft,
    build_diploma_conclusion_draft,
    build_diploma_full_draft,
    save_diploma_text,
)
from app.ml.diploma_defense_pack import (
    build_diploma_defense_speech,
    build_diploma_presentation_outline,
    save_diploma_text as save_defense_text,
)
from app.ml.dataset_cleaning_report import (
    build_cleaning_report,
    cleaning_report_to_markdown,
    save_cleaning_report_json,
    save_cleaning_report_markdown,
)
from app.ml.dataset_pipeline import (
    CANONICAL_COLUMNS,
    FEATURE_DATASET_COLUMNS,
    build_feature_rows,
    build_train_test_manifest,
    load_csv_rows,
    load_normalized_rows,
    normalize_rows,
    prepare_rows_for_normalization,
    save_csv_rows,
    save_json,
)
from app.ml.dataset_quality import (
    build_data_quality_report,
    quality_to_markdown,
    save_quality_json,
    save_quality_markdown,
)
from app.ml.dataset_profile import (
    build_dataset_profile,
    profile_to_markdown,
    save_profile_json,
    save_profile_markdown,
)
from app.ml.features import FEATURE_NAMES
from app.ml.statistical_model import (
    cross_validate_naive_bayes,
    evaluate_artifact,
    load_artifact,
    save_artifact,
    split_samples,
    split_samples_by_ids,
    train_naive_bayes,
)


def export_feature_dataset(
    input_path: Path | None = None,
    mapping_path: Path | None = None,
) -> dict[str, object]:
    source_path = input_path or settings.raw_dataset_path
    canonical_rows = load_normalized_rows(source_path, mapping_path=mapping_path)
    feature_rows = build_feature_rows(canonical_rows)
    split_manifest = build_train_test_manifest(feature_rows, train_ratio=0.8, seed=42)

    save_csv_rows(settings.canonical_dataset_path, canonical_rows, CANONICAL_COLUMNS)
    save_csv_rows(settings.feature_dataset_path, feature_rows, FEATURE_DATASET_COLUMNS)
    save_json(settings.dataset_split_path, split_manifest)

    return {
        "input_path": str(source_path),
        "mapping_path": str(mapping_path) if mapping_path is not None else None,
        "canonical_path": str(settings.canonical_dataset_path),
        "feature_path": str(settings.feature_dataset_path),
        "split_manifest_path": str(settings.dataset_split_path),
        "rows_exported": len(feature_rows),
    }


def generate_dataset_profile(
    dataset_path: Path | None = None,
    mapping_path: Path | None = None,
) -> dict[str, object]:
    source_path = dataset_path or settings.raw_dataset_path
    canonical_rows = load_normalized_rows(source_path, mapping_path=mapping_path)
    profile = build_dataset_profile(canonical_rows, source_path)
    save_profile_json(settings.dataset_profile_path, profile)
    save_profile_markdown(settings.dataset_profile_markdown_path, profile_to_markdown(profile))
    return {
        "profile_json_path": str(settings.dataset_profile_path),
        "profile_markdown_path": str(settings.dataset_profile_markdown_path),
        "mapping_path": str(mapping_path) if mapping_path is not None else None,
        "rows": profile["total_rows"],
        "labels": profile["total_labels"],
    }


def generate_data_quality_report(dataset_path: Path | None = None) -> dict[str, object]:
    source_path = dataset_path or settings.canonical_dataset_path
    if not source_path.exists() and source_path == settings.canonical_dataset_path:
        export_feature_dataset()
    rows = load_csv_rows(source_path)
    report = build_data_quality_report(rows, source_path)
    save_quality_json(settings.data_quality_path, report)
    save_quality_markdown(settings.data_quality_markdown_path, quality_to_markdown(report))
    return {
        "quality_json_path": str(settings.data_quality_path),
        "quality_markdown_path": str(settings.data_quality_markdown_path),
        "warnings": len(report["warnings"]),
        "duplicate_rows": report["duplicate_rows"],
    }


def generate_cleaning_report(
    dataset_path: Path | None = None,
    mapping_path: Path | None = None,
) -> dict[str, object]:
    source_path = dataset_path or settings.raw_dataset_path
    raw_rows = load_csv_rows(source_path)
    prepared_rows = prepare_rows_for_normalization(raw_rows, mapping_path=mapping_path)
    normalized_rows = normalize_rows(prepared_rows)
    report = build_cleaning_report(
        source_path=source_path,
        raw_rows=raw_rows,
        prepared_rows=prepared_rows,
        normalized_rows=normalized_rows,
        mapping_path=mapping_path,
    )
    save_cleaning_report_json(settings.cleaning_report_path, report)
    save_cleaning_report_markdown(
        settings.cleaning_report_markdown_path,
        cleaning_report_to_markdown(report),
    )
    return {
        "cleaning_json_path": str(settings.cleaning_report_path),
        "cleaning_markdown_path": str(settings.cleaning_report_markdown_path),
        "rows_with_any_change": report["rows_with_any_change"],
        "total_field_changes": report["total_field_changes"],
    }


def _load_feature_samples() -> list[dict[str, str]]:
    with settings.feature_dataset_path.open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def _save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _evaluation_to_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Respiratory NB Evaluation",
        "",
        f"- Samples: {report['samples']}",
        f"- Folds: {report['folds']}",
        f"- Mean accuracy: {report['mean_accuracy']}",
        f"- Overall accuracy: {report['overall_accuracy']}",
        "",
        "## Fold Results",
        "",
        "| Fold | Train | Test | Accuracy |",
        "| --- | ---: | ---: | ---: |",
    ]

    for result in report["fold_results"]:
        lines.append(
            f"| {result['fold']} | {result['train_samples']} | {result['test_samples']} | {result['accuracy']} |"
        )

    lines.extend(
        [
            "",
            "## Per Label Accuracy",
            "",
            "| Label | Accuracy |",
            "| --- | ---: |",
        ]
    )
    for label, accuracy in report["per_label_accuracy"].items():
        lines.append(f"| {label} | {accuracy} |")

    lines.extend(
        [
            "",
            "## Confusion Matrix",
            "",
            "| Expected | Predicted | Count |",
            "| --- | --- | ---: |",
        ]
    )
    for expected_label, predicted_counts in report["confusion_matrix"].items():
        for predicted_label, count in predicted_counts.items():
            lines.append(f"| {expected_label} | {predicted_label} | {count} |")

    return "\n".join(lines) + "\n"


def train_baseline_model() -> dict[str, object]:
    samples = _load_feature_samples()

    split_manifest: dict[str, object] | None = None
    if settings.dataset_split_path.exists():
        split_manifest = json.loads(settings.dataset_split_path.read_text(encoding="utf-8"))

    split_source = "random"
    if split_manifest is not None:
        train_samples, test_samples = split_samples_by_ids(
            samples,
            split_manifest.get("train_ids", []),
            split_manifest.get("test_ids", []),
        )
        if train_samples and test_samples:
            split_source = "manifest"
        else:
            train_samples, test_samples = split_samples(samples, train_ratio=0.8, seed=42)
    else:
        train_samples, test_samples = split_samples(samples, train_ratio=0.8, seed=42)

    artifact = train_naive_bayes(train_samples)
    metrics = evaluate_artifact(artifact, test_samples)

    save_artifact(settings.ml_model_path, artifact)

    payload = {
        "raw_dataset_path": str(settings.raw_dataset_path),
        "feature_dataset_path": str(settings.feature_dataset_path),
        "split_manifest_path": str(settings.dataset_split_path),
        "model_path": str(settings.ml_model_path),
        "train_samples": len(train_samples),
        "test_samples": len(test_samples),
        "feature_names": list(FEATURE_NAMES),
        "split_source": split_source,
        "metrics": metrics,
    }
    save_json(settings.ml_metrics_path, payload)
    return payload


def generate_model_evaluation(folds: int = 5) -> dict[str, object]:
    samples = _load_feature_samples()
    report = cross_validate_naive_bayes(samples, folds=folds, seed=42)
    save_json(settings.ml_evaluation_path, report)
    _save_text(settings.ml_evaluation_markdown_path, _evaluation_to_markdown(report))
    return {
        "evaluation_json_path": str(settings.ml_evaluation_path),
        "evaluation_markdown_path": str(settings.ml_evaluation_markdown_path),
        "folds": report["folds"],
        "overall_accuracy": report["overall_accuracy"],
    }


def generate_explainability_report(
    model_path: Path | None = None,
    top_n: int = 5,
) -> dict[str, object]:
    source_path = model_path or settings.ml_model_path
    if not source_path.exists() and source_path == settings.ml_model_path:
        train_baseline_model()
    artifact = load_artifact(source_path)
    report = build_explainability_report(artifact, top_n=top_n)
    save_explainability_json(settings.ml_explainability_path, report)
    save_explainability_markdown(
        settings.ml_explainability_markdown_path,
        explainability_to_markdown(report),
    )
    return {
        "explainability_json_path": str(settings.ml_explainability_path),
        "explainability_markdown_path": str(settings.ml_explainability_markdown_path),
        "labels": report["label_count"],
        "top_n": report["top_n"],
    }


def generate_diploma_results_report() -> dict[str, object]:
    profile = json.loads(settings.dataset_profile_path.read_text(encoding="utf-8")) if settings.dataset_profile_path.exists() else None
    quality = json.loads(settings.data_quality_path.read_text(encoding="utf-8")) if settings.data_quality_path.exists() else None
    cleaning = json.loads(settings.cleaning_report_path.read_text(encoding="utf-8")) if settings.cleaning_report_path.exists() else None
    metrics = json.loads(settings.ml_metrics_path.read_text(encoding="utf-8")) if settings.ml_metrics_path.exists() else None
    evaluation = json.loads(settings.ml_evaluation_path.read_text(encoding="utf-8")) if settings.ml_evaluation_path.exists() else None
    explainability = json.loads(settings.ml_explainability_path.read_text(encoding="utf-8")) if settings.ml_explainability_path.exists() else None

    report = build_diploma_results_report(
        profile=profile,
        quality=quality,
        cleaning=cleaning,
        metrics=metrics,
        evaluation=evaluation,
        explainability=explainability,
    )
    save_diploma_results_json(settings.diploma_report_path, report)
    save_diploma_results_markdown(
        settings.diploma_report_markdown_path,
        diploma_results_to_markdown(report),
    )
    return {
        "diploma_report_path": str(settings.diploma_report_path),
        "diploma_report_markdown_path": str(settings.diploma_report_markdown_path),
        "holdout_accuracy": report["performance_summary"]["holdout_accuracy"],
        "cv_accuracy": report["performance_summary"]["cv_accuracy"],
    }


def generate_diploma_chapter_draft() -> dict[str, object]:
    if not settings.diploma_report_path.exists():
        generate_diploma_results_report()

    report = json.loads(settings.diploma_report_path.read_text(encoding="utf-8"))
    content = build_diploma_chapter_draft(report)
    save_diploma_chapter_draft(settings.diploma_chapter_draft_path, content)
    return {
        "diploma_chapter_draft_path": str(settings.diploma_chapter_draft_path),
        "source_report_path": str(settings.diploma_report_path),
    }


def generate_diploma_supporting_drafts() -> dict[str, object]:
    if not settings.diploma_report_path.exists():
        generate_diploma_results_report()
    if not settings.diploma_chapter_draft_path.exists():
        generate_diploma_chapter_draft()

    report = json.loads(settings.diploma_report_path.read_text(encoding="utf-8"))
    chapter_3 = settings.diploma_chapter_draft_path.read_text(encoding="utf-8")

    chapter_1 = build_diploma_chapter_1_draft(report)
    chapter_2 = build_diploma_chapter_2_draft(report)
    conclusion = build_diploma_conclusion_draft(report)
    full_draft = build_diploma_full_draft(chapter_1, chapter_2, chapter_3, conclusion)

    save_diploma_text(settings.diploma_chapter_1_draft_path, chapter_1)
    save_diploma_text(settings.diploma_chapter_2_draft_path, chapter_2)
    save_diploma_text(settings.diploma_conclusion_draft_path, conclusion)
    save_diploma_text(settings.diploma_full_draft_path, full_draft)

    return {
        "chapter_1_path": str(settings.diploma_chapter_1_draft_path),
        "chapter_2_path": str(settings.diploma_chapter_2_draft_path),
        "chapter_3_path": str(settings.diploma_chapter_draft_path),
        "conclusion_path": str(settings.diploma_conclusion_draft_path),
        "full_draft_path": str(settings.diploma_full_draft_path),
        "source_report_path": str(settings.diploma_report_path),
    }


def generate_diploma_defense_pack() -> dict[str, object]:
    if not settings.diploma_report_path.exists():
        generate_diploma_results_report()

    report = json.loads(settings.diploma_report_path.read_text(encoding="utf-8"))
    presentation_outline = build_diploma_presentation_outline(report)
    defense_speech = build_diploma_defense_speech(report)

    save_defense_text(settings.diploma_presentation_outline_path, presentation_outline)
    save_defense_text(settings.diploma_defense_speech_path, defense_speech)

    return {
        "presentation_outline_path": str(settings.diploma_presentation_outline_path),
        "defense_speech_path": str(settings.diploma_defense_speech_path),
        "source_report_path": str(settings.diploma_report_path),
    }


def run_full_ml_pipeline(
    input_path: Path | None = None,
    mapping_path: Path | None = None,
) -> dict[str, object]:
    cleaning_result = generate_cleaning_report(dataset_path=input_path, mapping_path=mapping_path)
    export_result = export_feature_dataset(input_path=input_path, mapping_path=mapping_path)
    quality_result = generate_data_quality_report()
    profile_result = generate_dataset_profile(dataset_path=input_path, mapping_path=mapping_path)
    training_result = train_baseline_model()
    evaluation_result = generate_model_evaluation()
    explainability_result = generate_explainability_report()
    diploma_report_result = generate_diploma_results_report()
    diploma_chapter_result = generate_diploma_chapter_draft()
    diploma_supporting_drafts_result = generate_diploma_supporting_drafts()
    diploma_defense_pack_result = generate_diploma_defense_pack()
    return {
        "cleaning": cleaning_result,
        "export": export_result,
        "quality": quality_result,
        "profile": profile_result,
        "training": training_result,
        "evaluation": evaluation_result,
        "explainability": explainability_result,
        "diploma_report": diploma_report_result,
        "diploma_chapter": diploma_chapter_result,
        "diploma_supporting_drafts": diploma_supporting_drafts_result,
        "diploma_defense_pack": diploma_defense_pack_result,
    }
