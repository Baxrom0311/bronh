from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def get_connect_args(database_url: str) -> dict[str, Any]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _create_engine():
    engine_kwargs: dict[str, Any] = {"pool_pre_ping": True}
    connect_args = get_connect_args(settings.database_url)
    if connect_args:
        engine_kwargs["connect_args"] = connect_args
    return create_engine(settings.database_url, **engine_kwargs)


engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    if not settings.auto_create_tables:
        return

    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
