# Respiratory CDSS Defense Deck Plan

Audience: diplom himoya komissiyasi, ilmiy rahbar, texnik va amaliy qiymatni tez baholovchi tinglovchilar.

Objective: loyiha dolzarbligi, arxitekturasi, ML pipeline, explainability va amaliy natijalarini 10 slayd ichida tushunarli va himoya uchun ishlatishga tayyor ko'rinishda ko'rsatish.

Narrative arc:
- Muammo va dolzarblik
- Maqsad va vazifalar
- Tizim arxitekturasi
- Data va preprocessing
- Klinik qaror mantiqi
- Baholash natijalari
- Explainability va demo oqimi
- Cheklovlar
- Xulosa va keyingi ishlar

Slide list:
1. Cover: mavzu, qisqa framing, asosiy tezis
2. Muammo va dolzarblik
3. Maqsad va vazifalar
4. Tizim arxitekturasi
5. Ma'lumotlar va preprocessing
6. Klinik qaror mantiqi
7. Baholash natijalari
8. Explainability va demo oqimi
9. Cheklovlar
10. Xulosa va keyingi ishlar

Source plan:
- `backend/reports/diploma_ml_results.md`
- `backend/reports/diploma_presentation_outline.md`
- `backend/reports/diploma_defense_speech.md`
- `README.md`
- `backend/app/` va `frontend/src/` ichidagi arxitektura modullari

Visual system:
- 16:9 formal akademik deck
- Och ivory fon, yashil aksent, korall va oltin ikkilamchi ranglar
- Serif sarlavha (`Caladea`), sans body (`Lato`)
- Ochiq overlay, yumaloq kartalar, yuqorida nozik header rule

Imagegen plan:
- Joriy deck buildida reference image slotlari saqlanadi.
- Slayd mazmunining asosiy qismi editable PowerPoint shakllari va matn bloklari bilan beriladi.
- Reference PNGlar build va verification oqimini qo'llab-quvvatlash uchun alohida katalogda saqlanadi.

Asset needs:
- `tmp/slides/respiratory-cdss-defense/reference/slide-01.png` ... `slide-10.png`
- `tmp/slides/respiratory-cdss-defense/build/build_deck.mjs`

Editability plan:
- Barcha sarlavha, subtitle, kartalar va metric qiymatlar editable text box sifatida yoziladi.
- Har bir slayd speaker notes orqali presenter guidance va source mapping oladi.
- Final deliverable: bitta `.pptx` deck.
