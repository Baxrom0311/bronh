import json
from pathlib import Path

from app.ml.dataset_onboarding import build_onboarding_validation_report


def test_onboarding_validation_reports_missing_required_fields(tmp_path: Path):
    dataset_path = tmp_path / "dataset.csv"
    dataset_path.write_text(
        "temp,cough,days,label,extra_col\n38.5,dry,4,flu,unused\n",
        encoding="utf-8",
    )

    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps(
            {
                "fields": [
                    {
                        "canonical_field": "temperature",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["temperature", "temp"],
                    },
                    {
                        "canonical_field": "cough_type",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["cough_type", "cough"],
                    },
                    {
                        "canonical_field": "oxygen_saturation",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["spo2"],
                    },
                    {
                        "canonical_field": "diagnosis_label",
                        "required": True,
                        "source_column": "label",
                        "accepted_aliases": ["diagnosis_label", "label"],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    report = build_onboarding_validation_report(dataset_path, mapping_path)

    assert report["ready_for_pipeline"] is False
    assert report["alias_mappings"] == 2
    assert report["explicit_mappings"] == 1
    assert report["missing_required_fields"] == ["oxygen_saturation"]
    assert "extra_col" in report["unused_dataset_columns"]


def test_onboarding_validation_passes_when_required_columns_are_mapped(tmp_path: Path):
    dataset_path = tmp_path / "dataset.csv"
    dataset_path.write_text(
        "temp,cough,spo2,label\n38.5,dry,95,flu\n",
        encoding="utf-8",
    )

    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps(
            {
                "fields": [
                    {
                        "canonical_field": "temperature",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["temp"],
                    },
                    {
                        "canonical_field": "cough_type",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["cough"],
                    },
                    {
                        "canonical_field": "oxygen_saturation",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["spo2"],
                    },
                    {
                        "canonical_field": "diagnosis_label",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["label"],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    report = build_onboarding_validation_report(dataset_path, mapping_path)

    assert report["ready_for_pipeline"] is True
    assert report["missing_required_fields"] == []
    assert report["unused_dataset_columns"] == []


def test_onboarding_validation_flags_invalid_explicit_source_column(tmp_path: Path):
    dataset_path = tmp_path / "dataset.csv"
    dataset_path.write_text(
        "temp,cough,spo2,label\n38.5,dry,95,flu\n",
        encoding="utf-8",
    )

    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps(
            {
                "fields": [
                    {
                        "canonical_field": "temperature",
                        "required": True,
                        "source_column": "body_temp",
                        "accepted_aliases": ["temp"],
                    },
                    {
                        "canonical_field": "diagnosis_label",
                        "required": True,
                        "source_column": None,
                        "accepted_aliases": ["label"],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    report = build_onboarding_validation_report(dataset_path, mapping_path)

    assert report["ready_for_pipeline"] is False
    assert report["invalid_explicit_fields"] == ["temperature"]
    assert report["missing_required_fields"] == ["temperature"]
