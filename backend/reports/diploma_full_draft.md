# Diplom Ish Drafti

Quyidagi matn avtomatik generatsiya qilingan draft bo'lib, diplom talablari bo'yicha stilistik tahrir, adabiyotlar va rasm-jadvallar bilan boyitilishi kerak.

# 1-bob. Nafas yo'llari infeksiyalari uchun CDSS mavzusining dolzarbligi

## 1.1. Mavzuning dolzarbligi

Nafas yo'llari infeksiyalari keng tarqalgan klinik muammolardan biri bo'lib, ularni dastlabki bosqichda to'g'ri baholash kasallik og'irligini kamaytirish va bemorni to'g'ri yo'naltirish uchun muhim hisoblanadi. Ayniqsa, simptomlar o'xshash bo'lgan holatlarda shifokor yoki feldsher uchun tezkor va izohlanadigan qaror ko'magi kerak bo'ladi.

Mazkur loyiha ana shu ehtiyojdan kelib chiqib, simptomlar, hayotiy ko'rsatkichlar va epidemiologik omillar asosida dastlabki baholash beruvchi klinik qarorlarni qo'llab-quvvatlash tizimini ishlab chiqishga qaratilgan.

## 1.2. Tadqiqot maqsadi va vazifalari

Tadqiqotning asosiy maqsadi nafas yo'llari infeksiyalari simptomlari asosida dastlabki klinik baholashni amalga oshiruvchi, izohlanadigan va kengaytiriladigan CDSS prototipini ishlab chiqishdan iborat.

Ushbu maqsadga erishish uchun quyidagi vazifalar belgilandi:
- nafas yo'llari infeksiyalariga oid simptomlar va tegishli klinik indikatorlarni tizimlashtirish;
- bemor, simptom, tashxis va foydalanuvchi rollarini qamrab olgan dasturiy arxitekturani yaratish;
- rule-based klinik qoidalar va baseline ML modelini bitta baholash oqimiga birlashtirish;
- preprocessing, dataset quality, explainability va evaluation artefaktlarini tayyorlash;
- doktor va administrator uchun tasdiqlash hamda monitoring imkoniyatlarini yaratish;
- diplom yozuvi uchun natijalarni draft hisobotlar ko'rinishida avtomatlashtirish.

## 1.3. Tadqiqot obyekti va predmeti

Tadqiqot obyekti sifatida nafas yo'llari infeksiyalarini dastlabki bosqichda baholash jarayoni olindi. Tadqiqot predmeti esa ushbu jarayonni raqamli tizim yordamida simptomlar, klinik qoidalar va statistik model asosida qo'llab-quvvatlash mexanizmlaridan iborat.

## 1.4. Tadqiqotning amaliy ahamiyati

Ishlab chiqilgan prototip bemor simptomlarini standart ko'rinishda yig'ish, ularni dastlabki risk baholashga aylantirish, natijani izohlash va shifokor tasdig'ini saqlash imkonini beradi. Shu jihatdan loyiha telemeditsina, qabul bo'limi va birlamchi bo'g'indagi skrining vazifalari uchun mos yo'nalish beradi.

Joriy prototip bosqichida 203 ta yozuv va 7 ta labelga ega seed dataset asosida pipeline shakllantirilgan. Bu yakuniy klinik yechim emas, lekin real dataset kelganda tez qayta o'qitish va taqqoslashga tayyor infratuzilmani beradi.

## 1.5. Ishning tuzilmasi

Diplom ishi mantiqan uchta asosiy yo'nalishga bo'linadi: mavzuning nazariy va amaliy dolzarbligi, tizimni loyihalash va ishlab chiqish bosqichi hamda modelni baholash natijalari. Joriy prototipdan kelib chiqib, keyingi amaliy ustuvor yo'nalishlar quyidagicha shakllanadi:
- Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.
- NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.
- Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.
- Deduplication bosqichini cleaning pipeline ga qo'shing.

[Izoh: 1-bob uchun adabiyotlar sharhi, mavjud tizimlar tahlili va normativ manbalar qo'lda to'ldirilishi kerak.]


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


# 3-bob. CDSS modelini ishlab chiqish va baholash natijalari

## 3.1. Tadqiqot ma'lumotlari tavsifi

Ushbu bosqichda nafas yo'llari infeksiyalariga oid simptomlar asosida dastlabki baholashni amalga oshiruvchi model uchun tayyorlangan dataset va undan olingan natijalar tahlil qilindi.

Joriy artefaktlarga ko'ra dataset hajmi 203 ta qatorni, sinflar soni esa 7 tani tashkil etdi. Train va test tanlamalari mos ravishda 162 va 41 ta yozuvdan iborat bo'ldi.

Eng ko'p uchragan sinflar:
- ARVI / oddiy shamollash: 29
- Astma xuruji: 29
- Bronxit: 29

Eng ko'p missing kuzatilgan maydonlar:
- chronic_diseases: 154
- temperature: 0
- cough_type: 0

## 3.2. Preprocessing va data quality bosqichi

Preprocessing jarayonida ustunlar canonical formatga keltirildi, boolean va enum qiymatlar normallashtirildi hamda data quality tekshiruvlari bajarildi.

Data quality hisobotiga ko'ra duplicate qatorlar soni 5 ta, class balance ratio esa 1.0 ga teng bo'ldi. Cleaning report bo'yicha 0 ta qatorda o'zgarish aniqlanib, jami 0 ta maydon transformatsiya qilindi.

Asosiy sifat ogohlantirishlari:
- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

Default qiymat bilan to'ldirilgan asosiy maydonlar:
- chronic_diseases: 154

## 3.3. Modelni o'qitish va baholash

Bazaviy model sifatida categorical Naive Bayes yondashuvi ishlatildi. Model holdout va cross-validation orqali baholandi.

Natijalarga ko'ra holdout aniqligi 1.0, cross-validation aniqligi esa 0.995 ni tashkil etdi. Baholash 5 ta fold asosida amalga oshirildi.

Per-label bo'yicha eng yaxshi natijalar:
- ARVI / oddiy shamollash: 1.0
- Astma xuruji: 1.0
- Bronxit: 1.0

[Jadval 3.1 shu yerga qo'yiladi: modelning holdout va cross-validation natijalari]

## 3.4. Model interpretatsiyasi va explainability

Model natijalarining tushuntiriluvchanligini oshirish uchun har bir sinf uchun eng kuchli feature-signallar alohida ajratildi. Ushbu yondashuv klinik qarorni izohlashda qaysi simptom yoki belgilar kuchliroq ta'sir qilganini ko'rsatadi.

Explainability hisobotida 7 ta sinf va 18 ta feature qamrab olindi.

Global explainability highlightlar:
- ARVI / oddiy shamollash sinfi uchun `runny_nose = yes` belgisi kuchli signal bo'lib, support=4.883 va lift=132.0.
- COVID-19 (mumkin) sinfi uchun `loss_of_taste = yes` belgisi kuchli signal bo'lib, support=4.863 va lift=129.414.
- COVID-19 (mumkin) sinfi uchun `covid_contact = yes` belgisi kuchli signal bo'lib, support=4.863 va lift=129.414.
- Shoshilinch yordam kerak sinfi uchun `oxygen_bin = critical` belgisi kuchli signal bo'lib, support=4.816 va lift=123.519.
- Shoshilinch yordam kerak sinfi uchun `heart_rate_bin = very_high` belgisi kuchli signal bo'lib, support=4.772 va lift=118.148.

[Rasm 3.1 shu yerga qo'yiladi: explainability yoki SHAP natijalari]

## 3.5. Natijalarning cheklovlari

Olingan natijalarni talqin qilishda quyidagi cheklovlarni hisobga olish zarur. Ayniqsa, seed dataset sintetik bo'lgani sababli yuqori natijalar real klinik ma'lumotlarda qayta tekshirilishi kerak.

- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

## 3.6. Bob bo'yicha xulosa

Mazkur bobda CDSS tizimi uchun tayyorlangan bazaviy ML pipeline, preprocessing jarayoni, modelni baholash natijalari va explainability yondashuvi ko'rib chiqildi. Olingan natijalar prototip darajasida ijobiy bo'lsa-da, keyingi bosqichda real dataset asosida qayta o'qitish va kuchliroq model bilan taqqoslash talab etiladi.

Keyingi amaliy tavsiyalar:
- Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.
- NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.
- Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.
- Deduplication bosqichini cleaning pipeline ga qo'shing.
- Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.
- Default bilan to'ldirilgan ustunlarni tekshirib, real datasetda bu maydonlarni to'liqroq yig'ishga harakat qiling.

[Izoh: bu draft matn bo'lib, diplom talablari bo'yicha stilistik tahrir va adabiyotlar bilan boyitilishi kerak.]


# Xulosa

Diplom ishi doirasida nafas yo'llari infeksiyalari simptomlari asosida dastlabki baholashni amalga oshiruvchi klinik qarorlarni qo'llab-quvvatlash tizimining ishlaydigan prototipi yaratildi. Tizimda foydalanuvchini autentifikatsiya qilish, bemor ma'lumotlarini yuritish, simptomlarni baholash, tashxis natijasini izohlash, shifokor tasdig'i va administrator monitoringi birlashtirildi.

Asosiy amaliy natijalar:
- seed dataset hajmi: 203 ta yozuv;
- sinflar soni: 7 ta;
- holdout accuracy: 1.0;
- cross-validation accuracy: 0.995;
- explainability qamrovi: 7 ta sinf va 18 ta feature.

Shu bilan birga, loyiha faqat model yaratish bilan cheklanmay, balki preprocessing, data quality nazorati, dataset onboarding, cleaning comparison, explainability va diplom hisobotlarini avtomatik tayyorlash bosqichlarini ham qamrab oldi.

Ishning asosiy cheklovlari:
- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

Kelgusidagi ustuvor yo'nalishlar:
- Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.
- NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.
- Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.
- Deduplication bosqichini cleaning pipeline ga qo'shing.
- Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.
- Default bilan to'ldirilgan ustunlarni tekshirib, real datasetda bu maydonlarni to'liqroq yig'ishga harakat qiling.

Umuman olganda, ishlab chiqilgan prototip diplom ishining amaliy qismini shakllantirish uchun yetarli texnik poydevor yaratdi. Keyingi bosqichda real klinika ma'lumotlari bilan modelni qayta o'qitish, kuchliroq modellar bilan taqqoslash va klinik ekspertlar bilan validatsiya o'tkazish zarur.

