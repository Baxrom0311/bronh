from __future__ import annotations

from pathlib import Path
from typing import Any

from app.core.config import settings
from app.ml.features import (
    DIAGNOSIS_RISK_LEVEL,
    DIAGNOSIS_URGENCY_LEVEL,
    build_feature_vector_from_record,
    max_risk,
    max_urgency,
)
from app.ml.rules import rule_based_assessment
from app.ml.statistical_model import explain_prediction, load_artifact, predict_probabilities
from app.models.symptom_record import SymptomRecord


def _condition_recommendations(condition: str) -> list[str]:
    mapping = {
        "ARVI / oddiy shamollash": ["Ko'proq dam olish va suyuqlik ichish tavsiya etiladi."],
        "Gripp": ["Isitma va og'riq kuchaysa shifokor bilan bog'laning."],
        "Bronxit": ["Yo'tal 5 kundan ortsa qayta ko'rik tavsiya etiladi."],
        "Zotiljam (pnevmoniya)": ["Ko'krak og'rig'i yoki nafas yomonlashsa darhol shifokorga murojaat qiling."],
        "COVID-19 (mumkin)": ["Aloqani cheklash va alohida kuzatuv tavsiya etiladi."],
        "Astma xuruji": ["Inhaler rejimi va tezkor klinik baholash muhim."],
        "Shoshilinch yordam kerak": ["Tez yordam chaqirish yoki shoshilinch bo'limga borish kerak."],
    }
    return mapping.get(condition, [])


def _merge_unique(items: list[str], extra: list[str]) -> list[str]:
    result = list(items)
    for item in extra:
        if item not in result:
            result.append(item)
    return result


def _ensure_prediction_present(
    predictions: list[dict[str, float | str]],
    predicted_condition: str,
    confidence_score: float,
) -> list[dict[str, float | str]]:
    if any(item["disease"] == predicted_condition for item in predictions):
        return predictions
    return [{"disease": predicted_condition, "confidence": round(confidence_score, 3)}, *predictions[:2]]


def _override_with_rules(predicted_condition: str, rule_result: dict[str, object]) -> str:
    if rule_result["predicted_condition"] == "Shoshilinch yordam kerak":
        return "Shoshilinch yordam kerak"
    if rule_result["risk_level"] == "critical":
        return "Shoshilinch yordam kerak"
    return predicted_condition


def _build_explanation_payload(
    engine_mode: str,
    final_condition: str,
    rule_signals: dict[str, float],
    model_support: dict[str, Any] | None,
    override_applied: bool,
) -> dict[str, Any]:
    return {
        "engine_mode": engine_mode,
        "final_condition": final_condition,
        "override_applied": override_applied,
        "rule_signals": rule_signals,
        "model_support": model_support,
    }


class HybridCDSSEngine:
    def __init__(self) -> None:
        self.model_path = settings.ml_model_path
        self.model_artifact = self._load_model_artifact(self.model_path)
        self.model_ready = self.model_artifact is not None
        self.mode = "hybrid-ready" if self.model_ready else "rules-only"

    def predict(self, record: SymptomRecord) -> dict[str, object]:
        rule_result = rule_based_assessment(record)
        if not self.model_ready or self.model_artifact is None:
            return {
                **rule_result,
                "explanation": _build_explanation_payload(
                    engine_mode="rules-only",
                    final_condition=str(rule_result["predicted_condition"]),
                    rule_signals=dict(rule_result["explanation"]),
                    model_support=None,
                    override_applied=False,
                ),
                "summary": f"{rule_result['summary']} Engine: rules-only.",
            }

        feature_vector = build_feature_vector_from_record(record)
        ranked = predict_probabilities(self.model_artifact, feature_vector)
        model_condition, model_confidence = ranked[0]
        predicted_condition = _override_with_rules(model_condition, rule_result)
        model_support = explain_prediction(self.model_artifact, feature_vector)

        model_risk = DIAGNOSIS_RISK_LEVEL.get(model_condition, "medium")
        model_urgency = DIAGNOSIS_URGENCY_LEVEL.get(model_condition, "24_soat")
        risk_level = max_risk(model_risk, str(rule_result["risk_level"]))
        urgency_level = max_urgency(model_urgency, str(rule_result["urgency_level"]))

        top_predictions = [
            {"disease": label, "confidence": round(probability, 3)}
            for label, probability in ranked[:3]
        ]

        confidence_score = round(model_confidence, 3)
        if predicted_condition == "Shoshilinch yordam kerak":
            confidence_score = max(confidence_score, float(rule_result["confidence_score"]))
            top_predictions = _ensure_prediction_present(top_predictions, predicted_condition, confidence_score)

        recommendations = _merge_unique(
            list(rule_result["recommendations"]),
            _condition_recommendations(model_condition),
        )

        return {
            "predicted_condition": predicted_condition,
            "confidence_score": confidence_score,
            "risk_level": risk_level,
            "urgency_level": urgency_level,
            "top_predictions": top_predictions,
            "rule_engine_alerts": rule_result["rule_engine_alerts"],
            "recommendations": recommendations,
            "explanation": _build_explanation_payload(
                engine_mode="hybrid-ready",
                final_condition=predicted_condition,
                rule_signals=dict(rule_result["explanation"]),
                model_support=model_support,
                override_applied=predicted_condition != model_condition,
            ),
            "summary": (
                f"Asosiy baholash: {predicted_condition}. "
                f"ML confidence: {confidence_score}. "
                f"Xavf darajasi: {risk_level}. "
                f"Engine: hybrid-ready."
            ),
        }

    @staticmethod
    def _load_model_artifact(model_path: Path) -> dict[str, object] | None:
        if not model_path.exists():
            return None
        if model_path.suffix != ".json":
            return None
        return load_artifact(model_path)

    def reload(self) -> None:
        self.model_artifact = self._load_model_artifact(self.model_path)
        self.model_ready = self.model_artifact is not None
        self.mode = "hybrid-ready" if self.model_ready else "rules-only"


cdss_engine = HybridCDSSEngine()
