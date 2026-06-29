from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.symptom_record import CoughType, DyspneaLevel, HeadacheLevel


class SymptomRecordCreate(BaseModel):
    patient_id: str
    temperature: float = Field(ge=35.0, le=42.0)
    cough_type: CoughType = CoughType.none
    dyspnea_level: DyspneaLevel = DyspneaLevel.none
    sore_throat: bool = False
    runny_nose: bool = False
    headache_level: HeadacheLevel = HeadacheLevel.none
    muscle_pain: bool = False
    fatigue_level: int = Field(default=0, ge=0, le=10)
    duration_days: int = Field(ge=1, le=30)
    oxygen_saturation: float | None = Field(default=None, ge=70.0, le=100.0)
    heart_rate: int | None = Field(default=None, ge=40, le=200)
    respiratory_rate: int | None = Field(default=None, ge=10, le=60)
    chest_pain: bool = False
    loss_of_taste: bool = False
    diarrhea: bool = False
    chronic_diseases: list[str] = Field(default_factory=list)
    covid_contact: bool = False
    smoker: bool = False
    notes: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_severe_case_has_context(self) -> "SymptomRecordCreate":
        if self.dyspnea_level == DyspneaLevel.severe and self.oxygen_saturation is None:
            raise ValueError("oxygen_saturation is required for severe dyspnea")
        return self


class SymptomRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    submitted_by_user_id: str
    temperature: float
    cough_type: CoughType
    dyspnea_level: DyspneaLevel
    sore_throat: bool
    runny_nose: bool
    headache_level: HeadacheLevel
    muscle_pain: bool
    fatigue_level: int
    duration_days: int
    oxygen_saturation: float | None
    heart_rate: int | None
    respiratory_rate: int | None
    chest_pain: bool
    loss_of_taste: bool
    diarrhea: bool
    chronic_diseases: list[str]
    covid_contact: bool
    smoker: bool
    notes: str | None
    created_at: datetime
