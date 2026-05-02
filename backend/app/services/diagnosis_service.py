from sqlalchemy.orm import Session

from app.ml.model import cdss_engine
from app.models.diagnosis import Diagnosis
from app.models.symptom_record import SymptomRecord


def build_diagnosis(db: Session, record: SymptomRecord) -> Diagnosis:
    result = cdss_engine.predict(record)

    diagnosis = Diagnosis(
        record_id=record.id,
        predicted_condition=result["predicted_condition"],
        confidence_score=result["confidence_score"],
        risk_level=result["risk_level"],
        urgency_level=result["urgency_level"],
        top_predictions=result["top_predictions"],
        rule_engine_alerts=result["rule_engine_alerts"],
        recommendations=result["recommendations"],
        explanation=result["explanation"],
        summary=result["summary"],
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis
