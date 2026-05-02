from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.patient import Gender


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=255)
    date_of_birth: date
    gender: Gender
    height_cm: float | None = Field(default=None, ge=30, le=250)
    weight_kg: float | None = Field(default=None, ge=1, le=400)
    chronic_diseases: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    smoking_status: bool = False
    vaccination_status: dict[str, bool] = Field(default_factory=dict)
    emergency_contact: str | None = None


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    date_of_birth: date
    gender: Gender
    height_cm: float | None
    weight_kg: float | None
    chronic_diseases: list[str]
    allergies: list[str]
    smoking_status: bool
    vaccination_status: dict[str, bool]
    emergency_contact: str | None
    created_at: datetime
