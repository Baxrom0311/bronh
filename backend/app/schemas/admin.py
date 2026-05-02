from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import LanguageCode, UserRole


class AdminStatsRead(BaseModel):
    total_users: int
    total_patients: int
    total_symptom_records: int
    total_diagnoses: int
    confirmed_diagnoses: int
    users_by_role: dict[str, int]


class AdminUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    role: UserRole
    preferred_language: LanguageCode
    is_active: bool
    created_at: datetime
