from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.ml.metadata import get_model_metadata
from app.ml.model import cdss_engine
from app.models.user import User
from app.services.ml_pipeline_service import run_full_ml_pipeline

router = APIRouter(prefix="/admin/ml", tags=["admin-ml"])


@router.get("/metadata", summary="Admin uchun model metadata")
def admin_ml_metadata(_: User = Depends(require_roles("admin"))) -> dict[str, Any]:
    return get_model_metadata()


@router.post("/retrain", summary="ML pipeline ni qayta ishga tushirish")
def retrain_pipeline(_: User = Depends(require_roles("admin"))) -> dict[str, Any]:
    result = run_full_ml_pipeline()
    cdss_engine.reload()
    return {
        "status": "ok",
        "message": "ML pipeline qayta ishga tushirildi",
        "engine_mode": cdss_engine.mode,
        "result": result,
        "metadata": get_model_metadata(),
    }
