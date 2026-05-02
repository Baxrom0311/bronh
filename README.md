# Respiratory CDSS Diplom Project

Ushbu loyiha nafas yo'llari infeksiyalari simptomlari asosida dastlabki baholashni amalga oshiruvchi klinik qarorlarni qo'llab-quvvatlovchi tizim (CDSS) uchun boshlang'ich skeletdir.

Hozirgi bosqichda quyidagilar tayyor:

- `backend/` ichida FastAPI asosidagi ishlaydigan API skeleti
- JWT autentifikatsiya uchun boshlang'ich endpointlar
- bemor, simptom va tashxis oqimi uchun bazaviy ma'lumot modeli
- rule-based CDSS engine va pure-Python baseline ML modeli uchun tayyor arxitektura
- rule signallar va model feature support ni qaytaruvchi structured explanation qatlami
- Docker, `.env.example` va testlar
- `frontend/` ichida React 19 + TypeScript + TanStack Router + react-query frontend

## Tuzilma

```text
backend/
frontend/
docker-compose.yml
.env.example
README.md
```

## Tez ishga tushirish

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn main:app --reload
```

Swagger:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`
- `http://127.0.0.1:8000/openapi.json`

### 1.0.1. Swagger bilan ishlash

1. `POST /api/v1/auth/login` orqali `access_token` oling.
2. Swagger ichida `Authorize` tugmasini bosing.
3. Tokenni `Bearer <access_token>` ko'rinishida yuboring.
4. Keyin `patients -> symptoms -> diagnoses` oqimini sinab ko'ring.

Docs URL lar `.env` orqali boshqariladi:

```bash
CDSS_DOCS_URL=/docs
CDSS_REDOC_URL=/redoc
CDSS_OPENAPI_URL=/openapi.json
```

SQLite dev rejimida `CDSS_AUTO_CREATE_TABLES=true` bo'lsa jadvallar startup paytida avtomatik yaratiladi.

### 1.1. PostgreSQL + Alembic

PostgreSQL ishlatmoqchi bo'lsangiz `.env` ichida `CDSS_DATABASE_URL` ni yangilang:

```bash
CDSS_DATABASE_URL=postgresql+psycopg://cdss:cdss@localhost:5432/cdss
CDSS_AUTO_CREATE_TABLES=false
```

Migratsiya:

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

Alembic fayllari:

- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/20260421_0001_initial_schema.py`

### 2. Testlar

```bash
cd backend
pytest
```

### 3. To'liq ML pipeline

```bash
cd backend
source .venv/bin/activate
python scripts/run_ml_pipeline.py
# yoki real dataset bilan:
python scripts/run_ml_pipeline.py /absolute/path/to/real_dataset.csv
# yoki real dataset + mapping bilan:
python scripts/run_ml_pipeline.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json
```

Natija:

- `backend/data/respiratory_canonical_dataset.csv`
- `backend/data/respiratory_feature_dataset.csv`
- `backend/data/respiratory_train_test_split.json`
- `backend/data/respiratory_seed_profile.json`
- `backend/data/respiratory_seed_profile.md`
- `backend/data/respiratory_data_quality.json`
- `backend/data/respiratory_data_quality.md`
- `backend/data/respiratory_cleaning_report.json`
- `backend/data/respiratory_cleaning_report.md`
- `backend/ml_models/respiratory_nb_model.json`
- `backend/ml_models/respiratory_nb_metrics.json`
- `backend/ml_models/respiratory_nb_evaluation.json`
- `backend/ml_models/respiratory_nb_evaluation.md`
- `backend/ml_models/respiratory_nb_explainability.json`
- `backend/ml_models/respiratory_nb_explainability.md`
- `backend/reports/diploma_ml_results.json`
- `backend/reports/diploma_ml_results.md`
- `backend/reports/diploma_chapter_3_draft.md`
- `backend/reports/diploma_chapter_1_draft.md`
- `backend/reports/diploma_chapter_2_draft.md`
- `backend/reports/diploma_conclusion_draft.md`
- `backend/reports/diploma_full_draft.md`
- `backend/reports/diploma_presentation_outline.md`
- `backend/reports/diploma_defense_speech.md`

### 4. Dataset profilini alohida chiqarish

```bash
cd backend
source .venv/bin/activate
python scripts/generate_dataset_profile.py
# yoki real dataset bilan:
python scripts/generate_dataset_profile.py /absolute/path/to/real_dataset.csv
# yoki real dataset + mapping bilan:
python scripts/generate_dataset_profile.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json
```

Natija:

- `backend/data/respiratory_seed_profile.json`
- `backend/data/respiratory_seed_profile.md`

### 5. Data quality report

```bash
cd backend
source .venv/bin/activate
python scripts/generate_data_quality_report.py
# yoki canonical dataset bilan:
python scripts/generate_data_quality_report.py /absolute/path/to/canonical_dataset.csv
```

Natija:

- `backend/data/respiratory_data_quality.json`
- `backend/data/respiratory_data_quality.md`

### 6. Cleaning comparison report

```bash
cd backend
source .venv/bin/activate
python scripts/generate_cleaning_report.py
# yoki real dataset + mapping bilan:
python scripts/generate_cleaning_report.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json
```

Natija:

- `backend/data/respiratory_cleaning_report.json`
- `backend/data/respiratory_cleaning_report.md`

### 7. Canonical va feature dataset export

```bash
cd backend
source .venv/bin/activate
python scripts/export_feature_dataset.py
# yoki real dataset + mapping bilan:
python scripts/export_feature_dataset.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json
```

Natija:

- `backend/data/respiratory_canonical_dataset.csv`
- `backend/data/respiratory_feature_dataset.csv`
- `backend/data/respiratory_train_test_split.json`

### 8. Faqat model train qilish

```bash
cd backend
source .venv/bin/activate
python scripts/train_baseline_model.py
```

Model metadata endpointi endi holdout natijalar bilan birga stratified cross-validation evaluation reportini ham qaytaradi.

### 8.1. Explainability report

```bash
cd backend
source .venv/bin/activate
python scripts/generate_explainability_report.py
```

Natija:

- `backend/ml_models/respiratory_nb_explainability.json`
- `backend/ml_models/respiratory_nb_explainability.md`

### 8.2. Diplom uchun yakuniy natija report

```bash
cd backend
source .venv/bin/activate
python scripts/generate_diploma_results_report.py
```

Natija:

- `backend/reports/diploma_ml_results.json`
- `backend/reports/diploma_ml_results.md`

### 8.3. Diplom bobi uchun draft matn

```bash
cd backend
source .venv/bin/activate
python scripts/generate_diploma_chapter_draft.py
```

Natija:

- `backend/reports/diploma_chapter_3_draft.md`

### 8.4. Diplom uchun qolgan boblar va yakuniy draft

```bash
cd backend
source .venv/bin/activate
python scripts/generate_diploma_supporting_drafts.py
```

Natija:

- `backend/reports/diploma_chapter_1_draft.md`
- `backend/reports/diploma_chapter_2_draft.md`
- `backend/reports/diploma_conclusion_draft.md`
- `backend/reports/diploma_full_draft.md`

### 8.5. Himoya uchun prezentatsiya outline va nutq drafti

```bash
cd backend
source .venv/bin/activate
python scripts/generate_diploma_defense_pack.py
```

Natija:

- `backend/reports/diploma_presentation_outline.md`
- `backend/reports/diploma_defense_speech.md`

### 9. Real dataset validation

```bash
cd backend
source .venv/bin/activate
python scripts/validate_real_dataset.py /absolute/path/to/real_dataset.csv
```

Ixtiyoriy ikkinchi argument:

```bash
python scripts/validate_real_dataset.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json
```

Natija:

- `backend/data/real_dataset_mapping_template.json`
- `backend/data/real_dataset_validation.json`
- `backend/data/real_dataset_validation.md`

Tavsiya etilgan onboarding tartibi:

1. `python scripts/validate_real_dataset.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json`
2. `python scripts/generate_cleaning_report.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json`
3. `python scripts/run_ml_pipeline.py /absolute/path/to/real_dataset.csv /absolute/path/to/mapping.json`
4. `backend/notebooks/EDA.ipynb` ichida artefaktlarni tahlil qilish

### 10. Docker bilan

```bash
docker compose up --build
```

`docker compose` endi `postgres` servisni ham ko'taradi va backend ishga tushishidan oldin `alembic upgrade head` bajaradi.

### 11. XGBoost va SHAP notebooklari uchun optional dependency

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-ml.txt
```

So'ng:

```bash
cd backend
jupyter notebook notebooks/training_xgboost.ipynb
# yoki
jupyter notebook notebooks/interpretability_shap.ipynb
```

Eslatma:

- `backend/notebooks/training_xgboost.ipynb` `xgboost` bo'lmasa ham ochiladi, lekin training qismi avtomatik skip qilinadi.
- `backend/notebooks/interpretability_shap.ipynb` `shap` yoki `xgboost` bo'lmasa ham ochiladi, lekin SHAP qismi avtomatik skip qilinadi.

## Amaldagi endpointlar

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `GET /api/v1/health`
- `GET /api/v1/health/model-metadata`
- `GET /api/v1/admin/stats`
- `GET /api/v1/admin/users`
- `GET /api/v1/admin/ml/metadata`
- `POST /api/v1/admin/ml/retrain`
- `POST /api/v1/patients/`
- `GET /api/v1/patients/`
- `POST /api/v1/symptoms/`
- `GET /api/v1/symptoms/{record_id}`
- `POST /api/v1/diagnoses/`
- `GET /api/v1/diagnoses/{diagnosis_id}`
- `GET /api/v1/diagnoses/history`
- `POST /api/v1/diagnoses/{diagnosis_id}/confirm`

## Keyingi amaliy qadamlar

1. Dataset yig'ish va `backend/notebooks/` ichida EDA boshlash.
2. `backend/data/respiratory_seed_cases.csv` o'rniga real dataset qo'shish.
3. `scripts/export_feature_dataset.py` ni real dataset ustida ishlatish.
4. `scripts/run_ml_pipeline.py` ni real datasetga moslashtirish.
5. `backend/notebooks/training_xgboost.ipynb` orqali XGBoost comparisonni real datasetda ishga tushirish.
6. `backend/notebooks/interpretability_shap.ipynb` ni real dataset bilan ishga tushirish va rasm/jadval natijalarni diplomga chiqarish.
7. PostgreSQL + Alembic migratsiya oqimini amaliy holatga keltirish.
8. `frontend/` ichida doctor/admin panellarini alohida sahifalarga ajratish.
