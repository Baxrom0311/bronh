from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Respiratory CDSS API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"

    database_url: str = "sqlite:///./cdss.db"
    auto_create_tables: bool = True

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    ml_model_path: Path = Path("./ml_models/respiratory_nb_model.json")
    ml_metrics_path: Path = Path("./ml_models/respiratory_nb_metrics.json")
    ml_evaluation_path: Path = Path("./ml_models/respiratory_nb_evaluation.json")
    ml_evaluation_markdown_path: Path = Path("./ml_models/respiratory_nb_evaluation.md")
    ml_explainability_path: Path = Path("./ml_models/respiratory_nb_explainability.json")
    ml_explainability_markdown_path: Path = Path("./ml_models/respiratory_nb_explainability.md")
    diploma_report_path: Path = Path("./reports/diploma_ml_results.json")
    diploma_report_markdown_path: Path = Path("./reports/diploma_ml_results.md")
    diploma_chapter_draft_path: Path = Path("./reports/diploma_chapter_3_draft.md")
    diploma_chapter_1_draft_path: Path = Path("./reports/diploma_chapter_1_draft.md")
    diploma_chapter_2_draft_path: Path = Path("./reports/diploma_chapter_2_draft.md")
    diploma_conclusion_draft_path: Path = Path("./reports/diploma_conclusion_draft.md")
    diploma_full_draft_path: Path = Path("./reports/diploma_full_draft.md")
    diploma_presentation_outline_path: Path = Path("./reports/diploma_presentation_outline.md")
    diploma_defense_speech_path: Path = Path("./reports/diploma_defense_speech.md")
    raw_dataset_path: Path = Path("./data/respiratory_seed_cases.csv")
    canonical_dataset_path: Path = Path("./data/respiratory_canonical_dataset.csv")
    feature_dataset_path: Path = Path("./data/respiratory_feature_dataset.csv")
    dataset_split_path: Path = Path("./data/respiratory_train_test_split.json")
    dataset_profile_path: Path = Path("./data/respiratory_seed_profile.json")
    dataset_profile_markdown_path: Path = Path("./data/respiratory_seed_profile.md")
    data_quality_path: Path = Path("./data/respiratory_data_quality.json")
    data_quality_markdown_path: Path = Path("./data/respiratory_data_quality.md")
    cleaning_report_path: Path = Path("./data/respiratory_cleaning_report.json")
    cleaning_report_markdown_path: Path = Path("./data/respiratory_cleaning_report.md")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CDSS_",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def cors_allow_credentials(self) -> bool:
        return "*" not in self.cors_origins_list


settings = Settings()
