from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Integer, JSON, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CoughType(str, Enum):
    none = "none"
    dry = "dry"
    wet = "wet"
    bloody = "bloody"


class DyspneaLevel(str, Enum):
    none = "none"
    mild = "mild"
    moderate = "moderate"
    severe = "severe"


class HeadacheLevel(str, Enum):
    none = "none"
    mild = "mild"
    moderate = "moderate"
    severe = "severe"


class SymptomRecord(Base):
    __tablename__ = "symptom_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    submitted_by_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)

    temperature: Mapped[float] = mapped_column(Numeric(3, 1), nullable=False)
    cough_type: Mapped[CoughType] = mapped_column(SqlEnum(CoughType), default=CoughType.none, nullable=False)
    dyspnea_level: Mapped[DyspneaLevel] = mapped_column(SqlEnum(DyspneaLevel), default=DyspneaLevel.none, nullable=False)
    sore_throat: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    runny_nose: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    headache_level: Mapped[HeadacheLevel] = mapped_column(SqlEnum(HeadacheLevel), default=HeadacheLevel.none, nullable=False)
    muscle_pain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fatigue_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    oxygen_saturation: Mapped[float] = mapped_column(Numeric(4, 1), nullable=True)
    heart_rate: Mapped[int] = mapped_column(Integer, nullable=True)
    respiratory_rate: Mapped[int] = mapped_column(Integer, nullable=True)
    chest_pain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    loss_of_taste: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    diarrhea: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    chronic_diseases: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    covid_contact: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    smoker: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="symptom_records")
    diagnosis = relationship("Diagnosis", back_populates="record", uselist=False, cascade="all, delete-orphan")
