from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.database import get_db
from app.models.diagnosis import Diagnosis
from app.models.patient import Patient
from app.models.symptom_record import SymptomRecord
from app.models.user import User, UserRole
from app.schemas.admin import AdminStatsRead, AdminUserRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsRead, summary="Admin statistikani olish")
def admin_stats(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
) -> AdminStatsRead:
    users_by_role_rows = db.execute(
        select(User.role, func.count(User.id)).group_by(User.role).order_by(User.role)
    ).all()

    users_by_role = {role.value if isinstance(role, UserRole) else str(role): count for role, count in users_by_role_rows}

    return AdminStatsRead(
        total_users=db.scalar(select(func.count(User.id))) or 0,
        total_patients=db.scalar(select(func.count(Patient.id))) or 0,
        total_symptom_records=db.scalar(select(func.count(SymptomRecord.id))) or 0,
        total_diagnoses=db.scalar(select(func.count(Diagnosis.id))) or 0,
        confirmed_diagnoses=db.scalar(select(func.count(Diagnosis.id)).where(Diagnosis.is_confirmed.is_(True))) or 0,
        users_by_role=users_by_role,
    )


@router.get("/users", response_model=list[AdminUserRead], summary="Admin uchun userlar ro'yxati")
def admin_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc(), User.email.asc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())
