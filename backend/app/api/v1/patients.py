from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patients import PatientCreate, PatientRead

router = APIRouter(prefix="/patients", tags=["patients"])

PRIVILEGED_ROLES = {"doctor", "admin"}


def _can_access_patient(patient: Patient, user: User) -> bool:
    return user.role.value in PRIVILEGED_ROLES or patient.created_by_user_id == user.id


@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED, summary="Patient profilini yaratish")
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Patient:
    patient = Patient(
        **payload.model_dump(),
        created_by_user_id=current_user.id,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/", response_model=list[PatientRead], summary="Patientlar ro'yxatini olish")
def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Patient]:
    stmt = select(Patient).order_by(Patient.created_at.desc())
    if current_user.role.value not in PRIVILEGED_ROLES:
        stmt = stmt.where(Patient.created_by_user_id == current_user.id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{patient_id}", response_model=PatientRead, summary="Bitta patient profilini olish")
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Patient:
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if not _can_access_patient(patient, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return patient
