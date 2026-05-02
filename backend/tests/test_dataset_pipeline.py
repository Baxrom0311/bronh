import json

import pytest

from app.ml.dataset_pipeline import build_feature_rows, normalize_canonical_row, prepare_rows_for_normalization


def test_normalize_canonical_row_supports_aliases():
    row = {
        "temp": "38.5",
        "cough": "dry cough",
        "shortness_of_breath": "medium",
        "throat_pain": "yes",
        "fatigue": "8",
        "days": "4",
        "spo2": "95",
        "hr": "104",
        "rr": "22",
        "label": "influenza",
    }

    normalized = normalize_canonical_row(row)

    assert normalized["temperature"] == "38.5"
    assert normalized["cough_type"] == "dry"
    assert normalized["dyspnea_level"] == "moderate"
    assert normalized["sore_throat"] == "1"
    assert normalized["diagnosis_label"] == "Gripp"


def test_build_feature_rows_adds_sample_id_and_label():
    rows = [
        normalize_canonical_row(
            {
                "temperature": "37.2",
                "cough_type": "none",
                "dyspnea_level": "none",
                "diagnosis_label": "ARVI / oddiy shamollash",
            }
        )
    ]

    feature_rows = build_feature_rows(rows)

    assert feature_rows[0]["sample_id"] == "1"
    assert feature_rows[0]["label"] == "ARVI / oddiy shamollash"
    assert "temperature_bin" in feature_rows[0]


def test_prepare_rows_for_normalization_applies_explicit_mapping(tmp_path):
    rows = [
        {
            "body_temp": "38.5",
            "breathing_status": "medium",
            "cough_kind": "productive cough",
            "label_name": "influenza",
        }
    ]

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
                        "canonical_field": "dyspnea_level",
                        "required": True,
                        "source_column": "breathing_status",
                        "accepted_aliases": ["shortness_of_breath"],
                    },
                    {
                        "canonical_field": "cough_type",
                        "required": True,
                        "source_column": "cough_kind",
                        "accepted_aliases": ["cough"],
                    },
                    {
                        "canonical_field": "diagnosis_label",
                        "required": True,
                        "source_column": "label_name",
                        "accepted_aliases": ["label"],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    prepared_rows = prepare_rows_for_normalization(rows, mapping_path=mapping_path)
    normalized = normalize_canonical_row(prepared_rows[0])

    assert normalized["temperature"] == "38.5"
    assert normalized["dyspnea_level"] == "moderate"
    assert normalized["cough_type"] == "wet"
    assert normalized["diagnosis_label"] == "Gripp"


def test_prepare_rows_for_normalization_raises_for_missing_required_mapping(tmp_path):
    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps(
            {
                "fields": [
                    {
                        "canonical_field": "temperature",
                        "required": True,
                        "source_column": "missing_temp_column",
                        "accepted_aliases": ["temp"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Required fields are not mapped"):
        prepare_rows_for_normalization([{"temp": "37.1"}], mapping_path=mapping_path)


def test_prepare_rows_for_normalization_extracts_aliases_without_mapping():
    prepared_rows = prepare_rows_for_normalization(
        [
            {
                "temp": "38.5",
                "cough": "dry cough",
                "label": "influenza",
            }
        ]
    )

    assert prepared_rows[0]["temperature"] == "38.5"
    assert prepared_rows[0]["cough_type"] == "dry cough"
    assert prepared_rows[0]["diagnosis_label"] == "influenza"
