# Diplom Uchun ML Natijalari

## Qisqa Xulosa

- Dataset rows: `203`
- Labels: `7`
- Train/Test: `162` / `41`
- Holdout accuracy: `1.0`
- CV accuracy: `0.995`

## Dataset Holati

- Duplicate rows: `5`
- Class balance ratio: `1.0`
- Rows with cleaning changes: `0`
- Total field changes: `0`

### Eng ko'p uchragan label'lar
- ARVI / oddiy shamollash: 29
- Astma xuruji: 29
- Bronxit: 29

### Eng ko'p missing bo'lgan maydonlar
- chronic_diseases: 154
- temperature: 0
- cough_type: 0

## Model Baholash

- Folds: `5`
- CV mean accuracy: `0.995`
- Eng yaxshi per-label accuracy natijalari:
- ARVI / oddiy shamollash: 1.0
- Astma xuruji: 1.0
- Bronxit: 1.0

## Explainability Highlights

- ARVI / oddiy shamollash: runny_nose = yes | support=4.883 | lift=132.0
- COVID-19 (mumkin): loss_of_taste = yes | support=4.863 | lift=129.414
- COVID-19 (mumkin): covid_contact = yes | support=4.863 | lift=129.414
- Shoshilinch yordam kerak: oxygen_bin = critical | support=4.816 | lift=123.519
- Shoshilinch yordam kerak: heart_rate_bin = very_high | support=4.772 | lift=118.148

## Limitations

- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

## Tavsiyalar

- Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.
- NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.
- Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.
- Deduplication bosqichini cleaning pipeline ga qo'shing.
- Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.
- Default bilan to'ldirilgan ustunlarni tekshirib, real datasetda bu maydonlarni to'liqroq yig'ishga harakat qiling.
