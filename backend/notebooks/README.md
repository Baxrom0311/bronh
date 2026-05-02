# Notebooks Roadmap

Hozircha ML pipeline `scripts/train_baseline_model.py` orqali ishlaydi. Bu yondashuv tashqi kutubxonalarsiz tez prototip berish uchun tanlandi.

Notebook boshlashdan oldin quyidagi artefaktlarni generatsiya qilish tavsiya etiladi:

1. `../data/respiratory_seed_profile.json`
2. `../data/respiratory_data_quality.json`
3. `../ml_models/respiratory_nb_evaluation.json`
4. `../data/real_dataset_mapping_template.json`
5. `../data/real_dataset_validation.json`
6. `../data/respiratory_cleaning_report.json`
7. `../ml_models/respiratory_nb_explainability.json`

Tayyor notebook:

- `EDA.ipynb` - seed dataset, quality report, profile va model evaluation ni birlashtiruvchi bazaviy tahlil oqimi
- `training_xgboost.ipynb` - feature dataset asosida model comparison va XGBoost training skeleti
- `interpretability_shap.ipynb` - NB explainability artefakti va optional XGBoost + SHAP interpretatsiya oqimi

Eslatma:

- `training_xgboost.ipynb` dependency-aware yozilgan. Agar lokal muhitda `xgboost` bo'lmasa, notebook comparison skeleton sifatida qoladi va training celllarini skip qiladi.
- `interpretability_shap.ipynb` ham dependency-aware. `shap` yoki `xgboost` bo'lmasa, u NB explainability artefaktini ko'rsatib, SHAP qismini skip qiladi.
- XGBoost notebookni to'liq ishga tushirish uchun `cd ../ && source .venv/bin/activate && pip install -r requirements-ml.txt` dan foydalanish mumkin.

Real dataset onboarding:

1. `../data/real_dataset_mapping_template.json` ni to'ldiring.
2. `python scripts/validate_real_dataset.py /path/to/real_dataset.csv` bilan mapping tayyorligini tekshiring.
3. Kerak bo'lsa mapping faylini ikkinchi argument sifatida bering:
   `python scripts/validate_real_dataset.py /path/to/real_dataset.csv /path/to/mapping.json`
4. `python scripts/generate_cleaning_report.py /path/to/real_dataset.csv /path/to/mapping.json` bilan preprocessing o'zgarishlarini ko'ring.
5. `python scripts/run_ml_pipeline.py /path/to/real_dataset.csv /path/to/mapping.json` ni ishlating.
6. Profilni alohida chiqarish kerak bo'lsa:
   `python scripts/generate_dataset_profile.py /path/to/real_dataset.csv /path/to/mapping.json`
7. Exportni alohida chiqarish kerak bo'lsa:
   `python scripts/export_feature_dataset.py /path/to/real_dataset.csv /path/to/mapping.json`
8. So'ng `EDA.ipynb` ichida yangi artefaktlarni tahlil qiling.

Keyingi bosqichlar:

1. `EDA.ipynb` ni real dataset ustida ustun mapping va cleaning qadamlariga kengaytirish.
2. `training_xgboost.ipynb` ni real dataset va to'liq dependency bilan ishga tushirish.
3. `interpretability_shap.ipynb` ni real dataset va to'liq dependency bilan ishga tushirish.
