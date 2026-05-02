from fastapi import APIRouter

from app.api.v1 import admin, admin_ml, auth, diagnoses, health, patients, symptoms

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(symptoms.router)
api_router.include_router(diagnoses.router)
api_router.include_router(admin.router)
api_router.include_router(admin_ml.router)
