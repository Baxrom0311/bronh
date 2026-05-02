from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Enum as SqlEnum, ForeignKey, JSON, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Gender(str, Enum):
    male = "male"
    female = "female"


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_by_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Gender] = mapped_column(SqlEnum(Gender), nullable=False)
    height_cm: Mapped[float] = mapped_column(Numeric(5, 1), nullable=True)
    weight_kg: Mapped[float] = mapped_column(Numeric(5, 1), nullable=True)
    chronic_diseases: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    smoking_status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    vaccination_status: Mapped[dict[str, bool]] = mapped_column(JSON, default=dict, nullable=False)
    emergency_contact: Mapped[str] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    symptom_records = relationship("SymptomRecord", back_populates="patient", cascade="all, delete-orphan")
