# Himoya Uchun Prezentatsiya Rejasi

## Slayd 1. Mavzu va maqsad
- Mavzu: nafas yo'llari infeksiyalari simptomlari asosida dastlabki baholashni amalga oshiruvchi CDSS
- Maqsad: izohlanadigan va kengaytiriladigan klinik qarorlarni qo'llab-quvvatlash prototipini yaratish
- Natija: web ilova, ML pipeline va diplom hisobot artefaktlari

## Slayd 2. Muammo va dolzarblik
- Nafas yo'llari kasalliklarida simptomlar o'xshash bo'lishi sababli dastlabki baholash qiyinlashadi
- Birlamchi bo'g'in va skrining bosqichida tezkor, izohlanadigan qaror ko'magi kerak
- Tizim bemorni to'g'ri yo'naltirish va xavfli holatlarni ajratishga yordam beradi

## Slayd 3. Qo'yilgan vazifalar
- simptomlar va klinik indikatorlarni formal ko'rinishga keltirish
- backend, frontend va ma'lumotlar bazasi arxitekturasini qurish
- rule-based va baseline ML modelni bitta oqimga birlashtirish
- evaluation, explainability va diplom hisobotlarini avtomatlashtirish

## Slayd 4. Tizim arxitekturasi
- Frontend: React + TypeScript
- Backend: FastAPI + SQLAlchemy + JWT autentifikatsiya
- DB: SQLite dev rejimi, PostgreSQL + Alembic production yo'nalishi
- Rollar: patient, doctor, admin
- API modullar: auth, patients, symptoms, diagnoses, admin, admin_ml

## Slayd 5. Ma'lumotlar va preprocessing
- Dataset hajmi: 203 ta yozuv
- Label soni: 7 ta
- Train/Test: 162 / 41
- Cleaning o'zgarishi bo'lgan qatorlar: 0
- Transformatsiya qilingan maydonlar: 0
- Canonical schema, feature dataset va split manifest shakllantirilgan

Ko'zga tashlangan maydonlar:
- chronic_diseases: 154
- temperature: 0
- cough_type: 0

## Slayd 6. Klinik qaror mantiqi
- Rule-based qoidalar xavfli klinik holatlarni ajratadi
- Categorical Naive Bayes baseline model ehtimoliy qo'llab-quvvatlash beradi
- Natijada tashxis, risk darajasi va structured explanation qaytariladi
- Doctor tasdiqlashi va admin monitoringi qo'llab-quvvatlanadi

## Slayd 7. Baholash natijalari
- Holdout aniqligi: 1.0
- Cross-validation aniqligi: 0.995
- Fold soni: 5
- Seed datasetda yuqori natija olingan, lekin bu yakuniy klinik xulosa emas

Eng yaxshi per-label natijalar:
- ARVI / oddiy shamollash: 1.0
- Astma xuruji: 1.0
- Bronxit: 1.0

## Slayd 8. Explainability va demo oqimi
- Explainability qamrovi: 7 ta sinf, 18 ta feature
- UI da symptom assessment, review queue va admin panel mavjud
- Diagnosis javobida rule signals va model support alohida ko'rsatiladi
- Doctor tashxisni tasdiqlashi, admin esa stats va users ni ko'rishi mumkin

## Slayd 9. Cheklovlar
- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

## Slayd 10. Xulosa va keyingi ishlar
- Prototip darajasidagi CDSS tizimi to'liq ishlaydigan oqimga keltirildi
- ML pipeline, explainability va diplom matn draftlari avtomatlashtirildi
- Keyingi bosqichda real dataset bilan qayta trening va XGBoost taqqoslash zarur

Keyingi amaliy tavsiyalar:
- Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.
- NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.
- Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.
- Deduplication bosqichini cleaning pipeline ga qo'shing.
- Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.
