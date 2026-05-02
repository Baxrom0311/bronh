from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.models.diagnosis import Diagnosis
from app.models.symptom_record import SymptomRecord
from app.models.user import User
from app.schemas.diagnoses import DiagnosisConfirmRequest, DiagnosisCreateRequest, DiagnosisRead
from app.services.diagnosis_service import build_diagnosis

router = APIRouter(prefix="/diagnoses", tags=["diagnoses"])

PRIVILEGED_ROLES = {"doctor", "admin"}


@router.post("/", response_model=DiagnosisRead, status_code=status.HTTP_201_CREATED, summary="CDSS diagnosis yaratish")
def create_diagnosis(
    payload: DiagnosisCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Diagnosis:
    record = db.get(SymptomRecord, payload.record_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom record not found")
    if current_user.role.value not in PRIVILEGED_ROLES and record.submitted_by_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    existing = db.scalar(select(Diagnosis).where(Diagnosis.record_id == payload.record_id))
    if existing is not None and not payload.force_recompute:
        return existing

    if existing is not None and payload.force_recompute:
        db.delete(existing)
        db.commit()

    diagnosis = build_diagnosis(db=db, record=record)
    return diagnosis


@router.get("/history", response_model=list[DiagnosisRead], summary="Diagnosis tarixini olish")
def diagnosis_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Diagnosis]:
    stmt = select(Diagnosis).order_by(Diagnosis.created_at.desc())
    if current_user.role.value not in PRIVILEGED_ROLES:
        stmt = stmt.join(SymptomRecord).where(SymptomRecord.submitted_by_user_id == current_user.id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{diagnosis_id}", response_model=DiagnosisRead, summary="Bitta diagnosis natijasini olish")
def get_diagnosis(
    diagnosis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Diagnosis:
    diagnosis = db.get(Diagnosis, diagnosis_id)
    if diagnosis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")
    if current_user.role.value not in PRIVILEGED_ROLES and diagnosis.record.submitted_by_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return diagnosis


@router.post("/{diagnosis_id}/confirm", response_model=DiagnosisRead, summary="Doctor/admin tomonidan diagnosisni tasdiqlash")
def confirm_diagnosis(
    diagnosis_id: str,
    payload: DiagnosisConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("doctor", "admin")),
) -> Diagnosis:
    diagnosis = db.get(Diagnosis, diagnosis_id)
    if diagnosis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")

    diagnosis.is_confirmed = True
    diagnosis.confirmed_condition = (
        payload.confirmed_condition or diagnosis.confirmed_condition or diagnosis.predicted_condition
    )
    diagnosis.doctor_notes = payload.doctor_notes
    diagnosis.confirmed_by_user_id = current_user.id
    diagnosis.confirmed_at = datetime.now(UTC)
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis
