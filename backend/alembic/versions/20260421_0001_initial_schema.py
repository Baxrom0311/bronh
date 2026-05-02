"""initial schema

Revision ID: 20260421_0001
Revises:
Create Date: 2026-04-21 22:45:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260421_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


user_role_enum = sa.Enum("patient", "doctor", "admin", name="userrole")
language_code_enum = sa.Enum("uz", "ru", "en", name="languagecode")
gender_enum = sa.Enum("male", "female", name="gender")
cough_type_enum = sa.Enum("none", "dry", "wet", "bloody", name="coughtype")
dyspnea_level_enum = sa.Enum("none", "mild", "moderate", "severe", name="dyspnealevel")
headache_level_enum = sa.Enum("none", "mild", "moderate", "severe", name="headachelevel")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_enum, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("preferred_language", language_code_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "patients",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", gender_enum, nullable=False),
        sa.Column("height_cm", sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column("weight_kg", sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column("chronic_diseases", sa.JSON(), nullable=False),
        sa.Column("allergies", sa.JSON(), nullable=False),
        sa.Column("smoking_status", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("vaccination_status", sa.JSON(), nullable=False),
        sa.Column("emergency_contact", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auth_sessions_user_id"), "auth_sessions", ["user_id"], unique=False)

    op.create_table(
        "symptom_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("patient_id", sa.String(length=36), nullable=False),
        sa.Column("submitted_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("temperature", sa.Numeric(precision=3, scale=1), nullable=False),
        sa.Column("cough_type", cough_type_enum, nullable=False),
        sa.Column("dyspnea_level", dyspnea_level_enum, nullable=False),
        sa.Column("sore_throat", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("runny_nose", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("headache_level", headache_level_enum, nullable=False),
        sa.Column("muscle_pain", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("fatigue_level", sa.Integer(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("oxygen_saturation", sa.Numeric(precision=4, scale=1), nullable=True),
        sa.Column("heart_rate", sa.Integer(), nullable=True),
        sa.Column("respiratory_rate", sa.Integer(), nullable=True),
        sa.Column("chest_pain", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("loss_of_taste", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("diarrhea", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("chronic_diseases", sa.JSON(), nullable=False),
        sa.Column("covid_contact", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("smoker", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["submitted_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "diagnoses",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("record_id", sa.String(length=36), nullable=False),
        sa.Column("predicted_condition", sa.String(length=255), nullable=False),
        sa.Column("confidence_score", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("risk_level", sa.String(length=32), nullable=False),
        sa.Column("urgency_level", sa.String(length=32), nullable=False),
        sa.Column("top_predictions", sa.JSON(), nullable=False),
        sa.Column("rule_engine_alerts", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.JSON(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("is_confirmed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("confirmed_condition", sa.String(length=255), nullable=True),
        sa.Column("doctor_notes", sa.Text(), nullable=True),
        sa.Column("confirmed_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["confirmed_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["record_id"], ["symptom_records.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("record_id"),
    )


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_table("diagnoses")
    op.drop_table("symptom_records")
    op.drop_index(op.f("ix_auth_sessions_user_id"), table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_table("patients")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    if bind.dialect.name == "postgresql":
        headache_level_enum.drop(bind, checkfirst=True)
        dyspnea_level_enum.drop(bind, checkfirst=True)
        cough_type_enum.drop(bind, checkfirst=True)
        gender_enum.drop(bind, checkfirst=True)
        language_code_enum.drop(bind, checkfirst=True)
        user_role_enum.drop(bind, checkfirst=True)
