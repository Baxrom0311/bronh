from __future__ import annotations

from decimal import Decimal
from typing import Mapping


DIAGNOSIS_RISK_LEVEL: dict[str, str] = {
    "ARVI / oddiy shamollash": "low",
    "Gripp": "medium",
    "Bronxit": "medium",
    "Zotiljam (pnevmoniya)": "high",
    "COVID-19 (mumkin)": "high",
    "Astma xuruji": "high",
    "Shoshilinch yordam kerak": "critical",
}

DIAGNOSIS_URGENCY_LEVEL: dict[str, str] = {
    "ARVI / oddiy shamollash": "routine",
    "Gripp": "24_soat",
    "Bronxit": "24_soat",
    "Zotiljam (pnevmoniya)": "same_day",
    "COVID-19 (mumkin)": "same_day",
    "Astma xuruji": "same_day",
    "Shoshilinch yordam kerak": "immediate",
}

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
URGENCY_ORDER = {"routine": 0, "24_soat": 1, "same_day": 2, "immediate": 3}

FEATURE_NAMES = (
    "temperature_bin",
    "cough_type",
    "dyspnea_level",
    "sore_throat",
    "runny_nose",
    "headache_level",
    "muscle_pain",
    "fatigue_bin",
    "duration_bin",
    "oxygen_bin",
    "heart_rate_bin",
    "respiratory_rate_bin",
    "chest_pain",
    "loss_of_taste",
    "diarrhea",
    "covid_contact",
    "smoker",
    "chronic_bucket",
)


def _as_float(value: Decimal | float | int | str | None, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def _parse_bool(value: bool | str | int | None) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value == 1
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "ha", "y"}


def _yes_no(value: bool | str | int | None) -> str:
    return "yes" if _parse_bool(value) else "no"


def _enum_value(value: object, default: str = "none") -> str:
    if value is None or value == "":
        return default
    enum_value = getattr(value, "value", value)
    return str(enum_value or default)


def _split_chronic_diseases(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item.strip().lower() for item in value if item and item.strip()]
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def _temperature_bin(value: float) -> str:
    if value >= 39.5:
        return "very_high"
    if value >= 38.5:
        return "high"
    if value >= 37.5:
        return "mild"
    return "normal"


def _fatigue_bin(value: float) -> str:
    if value >= 8:
        return "severe"
    if value >= 5:
        return "moderate"
    if value >= 2:
        return "mild"
    return "none"


def _duration_bin(value: float) -> str:
    if value >= 8:
        return "long"
    if value >= 5:
        return "medium"
    return "short"


def _oxygen_bin(value: float) -> str:
    if value < 90:
        return "critical"
    if value < 94:
        return "low"
    if value < 97:
        return "borderline"
    return "normal"


def _heart_rate_bin(value: float) -> str:
    if value >= 130:
        return "very_high"
    if value >= 110:
        return "high"
    if value >= 90:
        return "mild"
    return "normal"


def _respiratory_rate_bin(value: float) -> str:
    if value >= 35:
        return "critical"
    if value >= 30:
        return "high"
    if value >= 21:
        return "mild"
    return "normal"


def _chronic_bucket(chronic_diseases: list[str]) -> str:
    diseases = set(chronic_diseases)
    if {"astma", "asthma"} & diseases:
        return "asthma"
    if {"koah", "copd"} & diseases:
        return "copd"
    if {"diabet", "diabetes"} & diseases:
        return "metabolic"
    if {"gipertoniya", "hypertension", "yurak", "cardiac"} & diseases:
        return "cardio"
    return "none"


def max_risk(first: str, second: str) -> str:
    return first if RISK_ORDER[first] >= RISK_ORDER[second] else second


def max_urgency(first: str, second: str) -> str:
    return first if URGENCY_ORDER[first] >= URGENCY_ORDER[second] else second


def build_feature_vector_from_mapping(row: Mapping[str, object]) -> dict[str, str]:
    chronic_diseases = _split_chronic_diseases(row.get("chronic_diseases"))  # type: ignore[arg-type]

    return {
        "temperature_bin": _temperature_bin(_as_float(row.get("temperature"), 36.6)),
        "cough_type": _enum_value(row.get("cough_type")),
        "dyspnea_level": _enum_value(row.get("dyspnea_level")),
        "sore_throat": _yes_no(row.get("sore_throat")),
        "runny_nose": _yes_no(row.get("runny_nose")),
        "headache_level": _enum_value(row.get("headache_level")),
        "muscle_pain": _yes_no(row.get("muscle_pain")),
        "fatigue_bin": _fatigue_bin(_as_float(row.get("fatigue_level"))),
        "duration_bin": _duration_bin(_as_float(row.get("duration_days"), 1)),
        "oxygen_bin": _oxygen_bin(_as_float(row.get("oxygen_saturation"), 98)),
        "heart_rate_bin": _heart_rate_bin(_as_float(row.get("heart_rate"), 80)),
        "respiratory_rate_bin": _respiratory_rate_bin(_as_float(row.get("respiratory_rate"), 18)),
        "chest_pain": _yes_no(row.get("chest_pain")),
        "loss_of_taste": _yes_no(row.get("loss_of_taste")),
        "diarrhea": _yes_no(row.get("diarrhea")),
        "covid_contact": _yes_no(row.get("covid_contact")),
        "smoker": _yes_no(row.get("smoker")),
        "chronic_bucket": _chronic_bucket(chronic_diseases),
    }


def build_feature_vector_from_record(record: object) -> dict[str, str]:
    return build_feature_vector_from_mapping(record.__dict__)
