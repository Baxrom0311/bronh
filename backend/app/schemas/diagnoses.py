from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DiagnosisCreateRequest(BaseModel):
    record_id: str
    force_recompute: bool = False


class DiagnosisConfirmRequest(BaseModel):
    confirmed_condition: str | None = None
    doctor_notes: str | None = None


class PredictionItem(BaseModel):
    disease: str
    confidence: float


class DiagnosisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    record_id: str
    predicted_condition: str
    confidence_score: float
    risk_level: str
    urgency_level: str
    top_predictions: list[dict[str, float | str]]
    rule_engine_alerts: list[str]
    recommendations: list[str]
    explanation: dict[str, Any]
    summary: str
    is_confirmed: bool
    confirmed_condition: str | None
    doctor_notes: str | None
    confirmed_by_user_id: str | None
    confirmed_at: datetime | None
    created_at: datetime
