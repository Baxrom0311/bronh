# 2-bob. CDSS tizimini loyihalash va dasturiy amalga oshirish

## 2.1. Tizimga qo'yilgan funksional talablar

Loyiha uchun asosiy funksional talablar sifatida foydalanuvchini ro'yxatdan o'tkazish va autentifikatsiya qilish, bemor profilini yaratish, simptomlarni kiritish, dastlabki tashxis olish, shifokor tomonidan tashxisni tasdiqlash hamda administrator uchun umumiy statistika va foydalanuvchi nazoratini ta'minlash belgilandi.

Amaldagi prototip quyidagi rollarni qo'llab-quvvatlaydi:
- `patient`: simptom kiritish va o'z tarixini ko'rish;
- `doctor`: tashxislar navbatini ko'rish va natijani tasdiqlash;
- `admin`: foydalanuvchilar va umumiy tizim statistikalarini kuzatish.

## 2.2. Dasturiy arxitektura

Tizim ko'p qatlamli arxitektura asosida ishlab chiqilgan. Frontend qismi React va TypeScript yordamida, backend esa FastAPI asosida yaratilgan. Ma'lumotlar qatlamida SQLAlchemy modeli ishlatiladi, rivojlantirilgan deploy oqimi uchun Alembic migratsiyalari va PostgreSQL qo'llab-quvvatlanadi.

Arxitekturaning asosiy qismlari:
- API routerlar: `health`, `auth`, `patients`, `symptoms`, `diagnoses`, `admin`, `admin_ml`;
- autentifikatsiya: JWT access/refresh tokenlar va session-backed refresh rotation;
- ma'lumotlar bazasi: SQLite dev rejimi va PostgreSQL production yo'nalishi;
- frontend workspace: assessment, review va admin ish maydonlari;
- ML va klinik mantiq qatlami: rule-based engine, Naive Bayes baseline, explainability hisobotlari.

## 2.3. Ma'lumotlar oqimi va preprocessing

Tizimga keladigan simptom ma'lumotlari avval canonical schema ga normallashtiriladi, so'ng feature datasetga o'tkaziladi va train/test split manifest bilan birga saqlanadi. Bu yondashuv real datasetlarni mapping orqali ulanganda ham pipeline ni bir xil saqlashga yordam beradi.

Joriy seed datasetda 203 ta yozuv mavjud bo'lib, cleaning reportga ko'ra 0 ta qatorda o'zgarish aniqlangan va 0 ta maydon transformatsiya qilingan.

Ko'zga tashlangan data-quality holatlari:
- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

Eng ko'p default bilan to'ldirilgan maydonlar:
- chronic_diseases: 154

## 2.4. Klinik qaror mantiqi va model qatlami

Dastlabki baholash gibrid yondashuv asosida qurilgan. Bir tomondan, klinik xavf holatlari uchun rule-based qoidalar ishlaydi. Ikkinchi tomondan, featurelar asosida categorical Naive Bayes baseline modeli ehtimoliy qo'llab-quvvatlash beradi. Natijada diagnosis javobida rule signallari va model support birga qaytariladi.

Joriy baholash bo'yicha holdout aniqligi 1.0, cross-validation aniqligi esa 0.995 ni tashkil etdi. Explainability hisobotida 7 ta sinf va 18 ta feature qamrab olindi.

## 2.5. Testlash va deploy tayyorgarligi

Backend qismida auth, diagnosis, dataset pipeline, explainability, admin va ML oqimlari uchun avtomatlashtirilgan testlar mavjud. Deploy tomonda Docker Compose, PostgreSQL servisi va `alembic upgrade head` oqimi tayyorlangan. Frontend esa build bosqichida tekshiriladi.

## 2.6. Bob bo'yicha xulosa

Mazkur bobda CDSS tizimining funksional talablari, dasturiy arxitekturasi, ma'lumotlar oqimi va model qatlamining amaliy tuzilmasi bayon qilindi. Shu bilan tizim keyingi bosqichda real dataset bilan qayta trening, XGBoost taqqoslash va klinik workflow chuqurlashtirish uchun tayyor platformaga aylandi.
