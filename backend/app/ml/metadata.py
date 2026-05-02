from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.ml.model import cdss_engine


def _read_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def get_model_metadata() -> dict[str, Any]:
    metrics = _read_json_if_exists(settings.ml_metrics_path)
    evaluation_report = _read_json_if_exists(settings.ml_evaluation_path)
    explainability_report = _read_json_if_exists(settings.ml_explainability_path)
    diploma_report = _read_json_if_exists(settings.diploma_report_path)
    cleaning_report = _read_json_if_exists(settings.cleaning_report_path)
    data_quality_report = _read_json_if_exists(settings.data_quality_path)
    dataset_profile = _read_json_if_exists(settings.dataset_profile_path)
    split_manifest = _read_json_if_exists(settings.dataset_split_path)

    return {
        "status": "ok",
        "engine_mode": cdss_engine.mode,
        "ml_model_ready": cdss_engine.model_ready,
        "model_path": str(settings.ml_model_path),
        "metrics_path": str(settings.ml_metrics_path),
        "evaluation_path": str(settings.ml_evaluation_path),
        "evaluation_markdown_path": str(settings.ml_evaluation_markdown_path),
        "explainability_path": str(settings.ml_explainability_path),
        "explainability_markdown_path": str(settings.ml_explainability_markdown_path),
        "diploma_report_path": str(settings.diploma_report_path),
        "diploma_report_markdown_path": str(settings.diploma_report_markdown_path),
        "diploma_chapter_draft_path": str(settings.diploma_chapter_draft_path),
        "diploma_chapter_1_draft_path": str(settings.diploma_chapter_1_draft_path),
        "diploma_chapter_2_draft_path": str(settings.diploma_chapter_2_draft_path),
        "diploma_conclusion_draft_path": str(settings.diploma_conclusion_draft_path),
        "diploma_full_draft_path": str(settings.diploma_full_draft_path),
        "diploma_presentation_outline_path": str(settings.diploma_presentation_outline_path),
        "diploma_defense_speech_path": str(settings.diploma_defense_speech_path),
        "cleaning_report_path": str(settings.cleaning_report_path),
        "cleaning_report_markdown_path": str(settings.cleaning_report_markdown_path),
        "data_quality_path": str(settings.data_quality_path),
        "data_quality_markdown_path": str(settings.data_quality_markdown_path),
        "feature_dataset_path": str(settings.feature_dataset_path),
        "dataset_split_path": str(settings.dataset_split_path),
        "dataset_profile_path": str(settings.dataset_profile_path),
        "metrics": metrics,
        "evaluation_report": evaluation_report,
        "explainability_report": explainability_report,
        "diploma_report": diploma_report,
        "cleaning_report": cleaning_report,
        "data_quality_report": data_quality_report,
        "split_manifest": split_manifest,
        "dataset_profile": dataset_profile,
    }
