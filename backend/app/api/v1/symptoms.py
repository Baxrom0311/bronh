from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.patient import Patient
from app.models.symptom_record import SymptomRecord
from app.models.user import User
from app.schemas.symptoms import SymptomRecordCreate, SymptomRecordRead

router = APIRouter(prefix="/symptoms", tags=["symptoms"])

PRIVILEGED_ROLES = {"doctor", "admin"}


@router.post("/", response_model=SymptomRecordRead, status_code=status.HTTP_201_CREATED, summary="Yangi symptom record yaratish")
def create_symptom_record(
    payload: SymptomRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SymptomRecord:
    patient = db.get(Patient, payload.patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if current_user.role.value not in PRIVILEGED_ROLES and patient.created_by_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    record = SymptomRecord(
        **payload.model_dump(),
        submitted_by_user_id=current_user.id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{record_id}", response_model=SymptomRecordRead, summary="Bitta symptom recordni olish")
def get_symptom_record(
    record_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SymptomRecord:
    record = db.get(SymptomRecord, record_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom record not found")
    if current_user.role.value not in PRIVILEGED_ROLES and record.submitted_by_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return record


@router.get("/", response_model=list[SymptomRecordRead], summary="Symptom recordlar ro'yxatini olish")
def list_symptom_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[SymptomRecord]:
    stmt = select(SymptomRecord).order_by(SymptomRecord.created_at.desc())
    if current_user.role.value not in PRIVILEGED_ROLES:
        stmt = stmt.where(SymptomRecord.submitted_by_user_id == current_user.id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())
