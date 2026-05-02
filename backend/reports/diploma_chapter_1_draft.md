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
