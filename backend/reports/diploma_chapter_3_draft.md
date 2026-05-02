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
