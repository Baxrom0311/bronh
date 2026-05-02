from fastapi import APIRouter

from app.core.config import settings
from app.ml.metadata import get_model_metadata
from app.ml.model import cdss_engine

router = APIRouter(tags=["health"])


@router.get("/health", summary="Service holatini tekshirish")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "engine_mode": cdss_engine.mode,
        "ml_model_ready": cdss_engine.model_ready,
    }


@router.get("/health/model-metadata", summary="Model metadata ni olish")
def model_metadata() -> dict[str, object]:
    return get_model_metadata()
