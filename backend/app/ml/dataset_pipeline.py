from __future__ import annotations

import csv
import json
import random
from collections import Counter
from pathlib import Path
from typing import Mapping

from app.ml.dataset_onboarding import apply_mapping_to_rows, load_mapping_template
from app.ml.features import FEATURE_NAMES, build_feature_vector_from_mapping

CANONICAL_COLUMNS = (
    "temperature",
    "cough_type",
    "dyspnea_level",
    "sore_throat",
    "runny_nose",
    "headache_level",
    "muscle_pain",
    "fatigue_level",
    "duration_days",
    "oxygen_saturation",
    "heart_rate",
    "respiratory_rate",
    "chest_pain",
    "loss_of_taste",
    "diarrhea",
    "covid_contact",
    "smoker",
    "chronic_diseases",
    "diagnosis_label",
)

FEATURE_DATASET_COLUMNS = ("sample_id", *FEATURE_NAMES, "label")

FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "temperature": ("temperature", "temp", "body_temperature", "fever_temp"),
    "cough_type": ("cough_type", "cough", "cough_kind"),
    "dyspnea_level": ("dyspnea_level", "breath_shortness", "shortness_of_breath"),
    "sore_throat": ("sore_throat", "throat_pain"),
    "runny_nose": ("runny_nose", "nasal_discharge", "cold"),
    "headache_level": ("headache_level", "headache"),
    "muscle_pain": ("muscle_pain", "myalgia", "body_ache"),
    "fatigue_level": ("fatigue_level", "fatigue", "tiredness"),
    "duration_days": ("duration_days", "days", "symptom_days"),
    "oxygen_saturation": ("oxygen_saturation", "spo2", "oxygen"),
    "heart_rate": ("heart_rate", "pulse", "hr"),
    "respiratory_rate": ("respiratory_rate", "rr", "breaths_per_minute"),
    "chest_pain": ("chest_pain", "chest_discomfort"),
    "loss_of_taste": ("loss_of_taste", "taste_loss", "anosmia"),
    "diarrhea": ("diarrhea", "diarrhoea"),
    "covid_contact": ("covid_contact", "covid_exposure", "contact"),
    "smoker": ("smoker", "smoking", "is_smoker"),
    "chronic_diseases": ("chronic_diseases", "comorbidities", "history"),
    "diagnosis_label": ("diagnosis_label", "label", "diagnosis", "target"),
}

ENUM_MAPS: dict[str, dict[str, str]] = {
    "cough_type": {
        "none": "none",
        "no": "none",
        "dry": "dry",
        "dry cough": "dry",
        "wet": "wet",
        "productive": "wet",
        "productive cough": "wet",
        "bloody": "bloody",
        "blood": "bloody",
        "bloody sputum": "bloody",
    },
    "dyspnea_level": {
        "none": "none",
        "no": "none",
        "mild": "mild",
        "moderate": "moderate",
        "medium": "moderate",
        "severe": "severe",
    },
    "headache_level": {
        "none": "none",
        "no": "none",
        "mild": "mild",
        "moderate": "moderate",
        "medium": "moderate",
        "severe": "severe",
    },
}

LABEL_MAP = {
    "arvi": "ARVI / oddiy shamollash",
    "cold": "ARVI / oddiy shamollash",
    "common cold": "ARVI / oddiy shamollash",
    "influenza": "Gripp",
    "flu": "Gripp",
    "gripp": "Gripp",
    "bronchitis": "Bronxit",
    "bronxit": "Bronxit",
    "pneumonia": "Zotiljam (pnevmoniya)",
    "zotiljam": "Zotiljam (pnevmoniya)",
    "covid": "COVID-19 (mumkin)",
    "covid-19": "COVID-19 (mumkin)",
    "asthma attack": "Astma xuruji",
    "asthma exacerbation": "Astma xuruji",
    "astma xuruji": "Astma xuruji",
    "emergency": "Shoshilinch yordam kerak",
    "urgent": "Shoshilinch yordam kerak",
    "critical": "Shoshilinch yordam kerak",
}

BOOL_TRUE = {"1", "true", "yes", "ha", "y"}
BOOL_FALSE = {"0", "false", "no", "yoq", "yo'q", "n", ""}

DEFAULTS = {
    "temperature": "36.6",
    "cough_type": "none",
    "dyspnea_level": "none",
    "sore_throat": "0",
    "runny_nose": "0",
    "headache_level": "none",
    "muscle_pain": "0",
    "fatigue_level": "0",
    "duration_days": "1",
    "oxygen_saturation": "98",
    "heart_rate": "80",
    "respiratory_rate": "18",
    "chest_pain": "0",
    "loss_of_taste": "0",
    "diarrhea": "0",
    "covid_contact": "0",
    "smoker": "0",
    "chronic_diseases": "",
    "diagnosis_label": "ARVI / oddiy shamollash",
}


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def save_csv_rows(path: Path, rows: list[dict[str, str]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def _get_first_value(row: Mapping[str, object], aliases: tuple[str, ...]) -> str:
    lowered = {str(key).strip().lower(): value for key, value in row.items()}
    for alias in aliases:
        if alias.lower() in lowered and lowered[alias.lower()] not in {None, ""}:
            return str(lowered[alias.lower()]).strip()
    return ""


def extract_canonical_row(row: Mapping[str, object]) -> dict[str, str]:
    return {
        field: _get_first_value(row, FIELD_ALIASES[field])
        for field in CANONICAL_COLUMNS
    }


def _normalize_bool(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in BOOL_TRUE:
        return "1"
    if lowered in BOOL_FALSE:
        return "0"
    return "1" if lowered else "0"


def _normalize_enum(field: str, value: str) -> str:
    lowered = value.strip().lower()
    if not lowered:
        return DEFAULTS[field]
    return ENUM_MAPS.get(field, {}).get(lowered, lowered)


def _normalize_label(value: str) -> str:
    lowered = value.strip().lower()
    if not lowered:
        return DEFAULTS["diagnosis_label"]
    return LABEL_MAP.get(lowered, value.strip())


def normalize_canonical_row(row: Mapping[str, object]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for field in CANONICAL_COLUMNS:
        raw_value = _get_first_value(row, FIELD_ALIASES[field])
        normalized[field] = raw_value or DEFAULTS[field]

    for field in ("sore_throat", "runny_nose", "muscle_pain", "chest_pain", "loss_of_taste", "diarrhea", "covid_contact", "smoker"):
        normalized[field] = _normalize_bool(normalized[field])

    for field in ("cough_type", "dyspnea_level", "headache_level"):
        normalized[field] = _normalize_enum(field, normalized[field])

    normalized["diagnosis_label"] = _normalize_label(normalized["diagnosis_label"])
    normalized["chronic_diseases"] = normalized["chronic_diseases"].strip().lower()
    return normalized


def normalize_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [normalize_canonical_row(row) for row in rows]


def prepare_rows_for_normalization(
    rows: list[dict[str, str]],
    mapping_path: Path | None = None,
) -> list[dict[str, str]]:
    if mapping_path is None:
        return [extract_canonical_row(row) for row in rows]
    mapping = load_mapping_template(mapping_path)
    return apply_mapping_to_rows(rows, mapping)


def load_normalized_rows(
    path: Path,
    mapping_path: Path | None = None,
) -> list[dict[str, str]]:
    raw_rows = load_csv_rows(path)
    prepared_rows = prepare_rows_for_normalization(raw_rows, mapping_path=mapping_path)
    return normalize_rows(prepared_rows)


def build_feature_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    feature_rows: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        feature_vector = build_feature_vector_from_mapping(row)
        feature_rows.append(
            {
                "sample_id": str(index),
                **feature_vector,
                "label": row["diagnosis_label"],
            }
        )
    return feature_rows


def build_train_test_manifest(feature_rows: list[dict[str, str]], train_ratio: float = 0.8, seed: int = 42) -> dict[str, object]:
    ids = [row["sample_id"] for row in feature_rows]
    shuffled = list(ids)
    random.Random(seed).shuffle(shuffled)
    train_size = max(1, int(len(shuffled) * train_ratio))
    train_ids = shuffled[:train_size]
    test_ids = shuffled[train_size:]

    label_by_id = {row["sample_id"]: row["label"] for row in feature_rows}
    train_distribution = Counter(label_by_id[sample_id] for sample_id in train_ids)
    test_distribution = Counter(label_by_id[sample_id] for sample_id in test_ids)

    return {
        "seed": seed,
        "train_ratio": train_ratio,
        "train_ids": train_ids,
        "test_ids": test_ids,
        "train_label_distribution": dict(sorted(train_distribution.items())),
        "test_label_distribution": dict(sorted(test_distribution.items())),
    }
