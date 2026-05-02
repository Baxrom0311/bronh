from decimal import Decimal

from app.models.symptom_record import CoughType, DyspneaLevel, HeadacheLevel, SymptomRecord


def _to_float(value: Decimal | float | int | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _base_scores() -> dict[str, float]:
    return {
        "ARVI / oddiy shamollash": 0.20,
        "Gripp": 0.18,
        "Bronxit": 0.16,
        "Zotiljam (pnevmoniya)": 0.12,
        "COVID-19 (mumkin)": 0.10,
        "Astma xuruji": 0.08,
        "Shoshilinch yordam kerak": 0.04,
    }


def rule_based_assessment(record: SymptomRecord) -> dict[str, object]:
    scores = _base_scores()
    alerts: list[str] = []
    explanation: dict[str, float] = {}

    temperature = _to_float(record.temperature) or 36.6
    oxygen = _to_float(record.oxygen_saturation)
    heart_rate = record.heart_rate or 0
    respiratory_rate = record.respiratory_rate or 0

    def boost(label: str, amount: float, feature: str) -> None:
        scores[label] += amount
        explanation[feature] = round(explanation.get(feature, 0.0) + amount, 3)

    if temperature >= 38.0:
        boost("Gripp", 0.25, "temperature")
        boost("Zotiljam (pnevmoniya)", 0.18, "temperature")
    if temperature >= 39.5:
        boost("Shoshilinch yordam kerak", 0.30, "temperature")
        alerts.append("Harorat juda yuqori. Bemorni tezkor ko'rikdan o'tkazish kerak.")

    if record.cough_type == CoughType.dry:
        boost("Gripp", 0.12, "cough_type")
        boost("COVID-19 (mumkin)", 0.20, "cough_type")
    if record.cough_type == CoughType.wet:
        boost("Bronxit", 0.25, "cough_type")
        boost("Zotiljam (pnevmoniya)", 0.20, "cough_type")
    if record.cough_type == CoughType.bloody:
        boost("Shoshilinch yordam kerak", 0.40, "cough_type")
        alerts.append("Qon aralash yo'tal aniqlandi.")

    if record.dyspnea_level == DyspneaLevel.mild:
        boost("Bronxit", 0.10, "dyspnea_level")
    if record.dyspnea_level == DyspneaLevel.moderate:
        boost("Zotiljam (pnevmoniya)", 0.28, "dyspnea_level")
        boost("Astma xuruji", 0.22, "dyspnea_level")
    if record.dyspnea_level == DyspneaLevel.severe:
        boost("Shoshilinch yordam kerak", 0.55, "dyspnea_level")
        boost("Astma xuruji", 0.25, "dyspnea_level")
        alerts.append("Og'ir nafas qisishi kuzatildi.")

    if record.sore_throat:
        boost("ARVI / oddiy shamollash", 0.18, "sore_throat")
    if record.runny_nose:
        boost("ARVI / oddiy shamollash", 0.18, "runny_nose")
    if record.muscle_pain:
        boost("Gripp", 0.14, "muscle_pain")
    if record.headache_level in {HeadacheLevel.moderate, HeadacheLevel.severe}:
        boost("Gripp", 0.10, "headache_level")
    if record.loss_of_taste:
        boost("COVID-19 (mumkin)", 0.36, "loss_of_taste")
    if record.covid_contact:
        boost("COVID-19 (mumkin)", 0.30, "covid_contact")
    if record.chest_pain:
        boost("Zotiljam (pnevmoniya)", 0.20, "chest_pain")
        boost("Shoshilinch yordam kerak", 0.20, "chest_pain")

    if record.duration_days >= 5:
        boost("Bronxit", 0.10, "duration_days")
        boost("Zotiljam (pnevmoniya)", 0.10, "duration_days")
    if record.duration_days >= 7:
        boost("COVID-19 (mumkin)", 0.08, "duration_days")

    if oxygen is not None and oxygen < 94:
        boost("Zotiljam (pnevmoniya)", 0.30, "oxygen_saturation")
        boost("Shoshilinch yordam kerak", 0.35, "oxygen_saturation")
        alerts.append("SpO2 pasaygan.")
    if oxygen is not None and oxygen < 90:
        boost("Shoshilinch yordam kerak", 0.30, "oxygen_saturation")
        alerts.append("SpO2 kritik darajada past. Tez yordam tavsiya etiladi.")

    if heart_rate >= 130:
        boost("Shoshilinch yordam kerak", 0.20, "heart_rate")
        alerts.append("Yurak urish tezligi yuqori.")
    if respiratory_rate >= 30:
        boost("Shoshilinch yordam kerak", 0.24, "respiratory_rate")
        boost("Zotiljam (pnevmoniya)", 0.18, "respiratory_rate")

    chronic = {item.lower() for item in record.chronic_diseases}
    if {"astma", "asthma"} & chronic:
        boost("Astma xuruji", 0.25, "chronic_diseases")
    if {"copd", "koah"} & chronic:
        boost("Shoshilinch yordam kerak", 0.18, "chronic_diseases")
        boost("Bronxit", 0.12, "chronic_diseases")

    total = sum(scores.values())
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_predictions = [
        {"disease": label, "confidence": round(score / total, 3)}
        for label, score in ranked[:3]
    ]

    predicted_condition = ranked[0][0]
    confidence_score = round(ranked[0][1] / total, 3)

    risk_level = "low"
    urgency_level = "routine"
    if predicted_condition in {"Gripp", "Bronxit"}:
        risk_level = "medium"
        urgency_level = "24_soat"
    if predicted_condition in {"Zotiljam (pnevmoniya)", "COVID-19 (mumkin)", "Astma xuruji"}:
        risk_level = "high"
        urgency_level = "same_day"
    if predicted_condition == "Shoshilinch yordam kerak":
        risk_level = "critical"
        urgency_level = "immediate"

    if oxygen is not None and oxygen < 90:
        predicted_condition = "Shoshilinch yordam kerak"
        risk_level = "critical"
        urgency_level = "immediate"

    recommendations = [
        "Natija klinik ko'rik o'rnini bosmaydi.",
        "Suyuqlik qabul qilish va dam olish tavsiya etiladi.",
    ]
    if risk_level == "medium":
        recommendations.append("24 soat ichida shifokor ko'rigidan o'tish tavsiya etiladi.")
    if risk_level == "high":
        recommendations.append("Bugunning o'zida shifokorga murojaat qiling.")
    if risk_level == "critical":
        recommendations = [
            "Tez yordam yoki shoshilinch tibbiy yordamga darhol murojaat qiling.",
            "Bemorni kuzatuvsiz qoldirmang.",
        ]
    if predicted_condition == "COVID-19 (mumkin)":
        recommendations.append("Aloqani cheklash va alohida kuzatuv tavsiya etiladi.")

    summary = (
        f"Asosiy baholash: {predicted_condition}. "
        f"Ishonch darajasi: {confidence_score}. "
        f"Xavf darajasi: {risk_level}."
    )

    if not alerts and risk_level in {"high", "critical"}:
        alerts.append("Risk yuqori. Klinik qayta baholash zarur.")

    return {
        "predicted_condition": predicted_condition,
        "confidence_score": confidence_score,
        "risk_level": risk_level,
        "urgency_level": urgency_level,
        "top_predictions": top_predictions,
        "rule_engine_alerts": alerts,
        "recommendations": recommendations,
        "explanation": dict(sorted(explanation.items(), key=lambda item: item[1], reverse=True)[:5]),
        "summary": summary,
    }
