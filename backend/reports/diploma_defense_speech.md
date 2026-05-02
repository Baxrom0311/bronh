# Himoya Uchun Nutq Drafti

Assalomu alaykum. Mening diplom ish mavzuyim nafas yo'llari infeksiyalari simptomlari asosida dastlabki baholashni amalga oshiruvchi klinik qarorlarni qo'llab-quvvatlovchi tizimni ishlab chiqishga bag'ishlangan.

Mazkur mavzuning dolzarbligi shundaki, nafas yo'llari kasalliklarida ko'plab simptomlar bir-biriga o'xshash bo'ladi. Shu sababli dastlabki bosqichda bemorning holatini tez va izohlanadigan tarzda baholash muhim ahamiyatga ega. Ayniqsa, skrining yoki birlamchi bo'g'inda shifokorga yoki tibbiy xodimga qo'shimcha qaror ko'magi kerak bo'ladi.

Ishimning asosiy maqsadi simptomlar, hayotiy ko'rsatkichlar va ayrim epidemiologik omillar asosida dastlabki baholash bera oladigan CDSS prototipini ishlab chiqishdan iborat bo'ldi. Ushbu maqsadga erishish uchun men backend, frontend, ma'lumotlar bazasi, rule-based qaror qatlami, baseline ML modeli va explainability mexanizmlarini yagona tizimga birlashtirdim.

Tizim arxitekturasi amaliy jihatdan uch qismdan iborat. Frontend qismi React va TypeScript asosida qurilgan bo'lib, unda patient, doctor va admin rollari uchun alohida ish oqimlari mavjud. Backend qismi FastAPI asosida yozilgan, autentifikatsiya JWT access va refresh tokenlar orqali amalga oshiriladi. Ma'lumotlar bazasi qatlamida SQLite dev rejimi va PostgreSQL plus Alembic migratsiya yo'nalishi tayyorlangan.

Model va data pipeline bosqichida 203 ta yozuv va 7 ta sinfni o'z ichiga olgan seed dataset bilan ishladim. Ma'lumotlar canonical schema ga normallashtirildi, feature dataset shakllantirildi va train/test split manifest yaratildi. Shuningdek, dataset profiling, data quality va cleaning reportlar avtomatik generatsiya qilindi.

Qaror mexanizmi gibrid yondashuv asosida ishlaydi. Bir tomondan, klinik xavf holatlarini aniqlovchi rule-based qoidalar mavjud. Ikkinchi tomondan, categorical Naive Bayes baseline modeli ehtimoliy qo'llab-quvvatlash beradi. Natijada tizim foydalanuvchiga nafaqat tashxis taxminini, balki ushbu natijani qo'llab-quvvatlagan signal va featurelarni ham ko'rsatadi.

Baholash natijalariga ko'ra holdout aniqligi 1.0, cross-validation aniqligi esa 0.995 ni tashkil etdi. Explainability hisobotida 7 ta sinf va 18 ta feature qamrab olindi. Bu ko'rsatkichlar prototip darajasida ijobiy natija berganini ko'rsatadi.

Shu bilan birga, natijalarni talqin qilishda cheklovlarni hisobga olish zarur. Joriy dataset kichik va sintetik bo'lgani sababli yuqori accuracy real klinik natija sifatida qabul qilinmaydi. Buni keyingi bosqichda real ochiq yoki klinik dataset bilan albatta qayta tekshirish kerak.

Asosiy cheklovlar:
- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

Xulosa qilib aytganda, men diplom ish doirasida ishlaydigan CDSS prototipini yaratdim. Tizimda foydalanuvchi oqimi, tashxislash, doctor tasdiqlashi, admin monitoringi, ML pipeline, explainability va diplom hisobotlari birlashtirildi.

Kelgusidagi ishlar sifatida quyidagilarni rejalashtiraman:
- Real klinik yoki ochiq dataset bilan pipeline ni qayta ishga tushirish.
- NB baseline natijalarini XGBoost va SHAP interpretatsiya bilan taqqoslash.
- Diplom matnida preprocessing, evaluation va explainability bosqichlarini alohida jadvallar bilan ko'rsatish.
- Deduplication bosqichini cleaning pipeline ga qo'shing.
- Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.

E'tiboringiz uchun rahmat. Savollaringiz bo'lsa, mamnuniyat bilan javob beraman.
