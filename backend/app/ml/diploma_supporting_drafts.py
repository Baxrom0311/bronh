from __future__ import annotations

from pathlib import Path
from typing import Any


def _bullet_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- Ma'lumot mavjud emas."]
    return [f"- {item}" for item in items]


def _top_item_lines(items: list[dict[str, Any]], suffix: str = "") -> list[str]:
    if not items:
        return ["- Ma'lumot mavjud emas."]
    return [f"- {item['name']}: {item['value']}{suffix}" for item in items]


def build_diploma_chapter_1_draft(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    recommendations = report["recommendations"]

    lines = [
        "# 1-bob. Nafas yo'llari infeksiyalari uchun CDSS mavzusining dolzarbligi",
        "",
        "## 1.1. Mavzuning dolzarbligi",
        "",
        (
            "Nafas yo'llari infeksiyalari keng tarqalgan klinik muammolardan biri bo'lib, "
            "ularni dastlabki bosqichda to'g'ri baholash kasallik og'irligini kamaytirish "
            "va bemorni to'g'ri yo'naltirish uchun muhim hisoblanadi. Ayniqsa, simptomlar "
            "o'xshash bo'lgan holatlarda shifokor yoki feldsher uchun tezkor va izohlanadigan "
            "qaror ko'magi kerak bo'ladi."
        ),
        "",
        (
            "Mazkur loyiha ana shu ehtiyojdan kelib chiqib, simptomlar, hayotiy ko'rsatkichlar "
            "va epidemiologik omillar asosida dastlabki baholash beruvchi klinik qarorlarni "
            "qo'llab-quvvatlash tizimini ishlab chiqishga qaratilgan."
        ),
        "",
        "## 1.2. Tadqiqot maqsadi va vazifalari",
        "",
        (
            "Tadqiqotning asosiy maqsadi nafas yo'llari infeksiyalari simptomlari asosida "
            "dastlabki klinik baholashni amalga oshiruvchi, izohlanadigan va kengaytiriladigan "
            "CDSS prototipini ishlab chiqishdan iborat."
        ),
        "",
        "Ushbu maqsadga erishish uchun quyidagi vazifalar belgilandi:",
        "- nafas yo'llari infeksiyalariga oid simptomlar va tegishli klinik indikatorlarni tizimlashtirish;",
        "- bemor, simptom, tashxis va foydalanuvchi rollarini qamrab olgan dasturiy arxitekturani yaratish;",
        "- rule-based klinik qoidalar va baseline ML modelini bitta baholash oqimiga birlashtirish;",
        "- preprocessing, dataset quality, explainability va evaluation artefaktlarini tayyorlash;",
        "- doktor va administrator uchun tasdiqlash hamda monitoring imkoniyatlarini yaratish;",
        "- diplom yozuvi uchun natijalarni draft hisobotlar ko'rinishida avtomatlashtirish.",
        "",
        "## 1.3. Tadqiqot obyekti va predmeti",
        "",
        (
            "Tadqiqot obyekti sifatida nafas yo'llari infeksiyalarini dastlabki bosqichda baholash "
            "jarayoni olindi. Tadqiqot predmeti esa ushbu jarayonni raqamli tizim yordamida "
            "simptomlar, klinik qoidalar va statistik model asosida qo'llab-quvvatlash "
            "mexanizmlaridan iborat."
        ),
        "",
        "## 1.4. Tadqiqotning amaliy ahamiyati",
        "",
        (
            "Ishlab chiqilgan prototip bemor simptomlarini standart ko'rinishda yig'ish, "
            "ularni dastlabki risk baholashga aylantirish, natijani izohlash va shifokor "
            "tasdig'ini saqlash imkonini beradi. Shu jihatdan loyiha telemeditsina, qabul "
            "bo'limi va birlamchi bo'g'indagi skrining vazifalari uchun mos yo'nalish beradi."
        ),
        "",
        (
            f"Joriy prototip bosqichida {dataset['total_rows']} ta yozuv va {dataset['total_labels']} ta "
            "labelga ega seed dataset asosida pipeline shakllantirilgan. Bu yakuniy klinik "
            "yechim emas, lekin real dataset kelganda tez qayta o'qitish va taqqoslashga tayyor "
            "infratuzilmani beradi."
        ),
        "",
        "## 1.5. Ishning tuzilmasi",
        "",
        (
            "Diplom ishi mantiqan uchta asosiy yo'nalishga bo'linadi: mavzuning nazariy va "
            "amaliy dolzarbligi, tizimni loyihalash va ishlab chiqish bosqichi hamda modelni "
            "baholash natijalari. Joriy prototipdan kelib chiqib, keyingi amaliy ustuvor yo'nalishlar "
            "quyidagicha shakllanadi:"
        ),
    ]
    lines.extend(_bullet_lines(recommendations[:4]))
    lines.extend(
        [
            "",
            "[Izoh: 1-bob uchun adabiyotlar sharhi, mavjud tizimlar tahlili va normativ manbalar qo'lda to'ldirilishi kerak.]",
            "",
        ]
    )
    return "\n".join(lines)


def build_diploma_chapter_2_draft(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    quality = report["quality_summary"]
    cleaning = report["cleaning_summary"]
    performance = report["performance_summary"]
    explainability = report["explainability_summary"]

    lines = [
        "# 2-bob. CDSS tizimini loyihalash va dasturiy amalga oshirish",
        "",
        "## 2.1. Tizimga qo'yilgan funksional talablar",
        "",
        (
            "Loyiha uchun asosiy funksional talablar sifatida foydalanuvchini ro'yxatdan o'tkazish "
            "va autentifikatsiya qilish, bemor profilini yaratish, simptomlarni kiritish, dastlabki "
            "tashxis olish, shifokor tomonidan tashxisni tasdiqlash hamda administrator uchun umumiy "
            "statistika va foydalanuvchi nazoratini ta'minlash belgilandi."
        ),
        "",
        "Amaldagi prototip quyidagi rollarni qo'llab-quvvatlaydi:",
        "- `patient`: simptom kiritish va o'z tarixini ko'rish;",
        "- `doctor`: tashxislar navbatini ko'rish va natijani tasdiqlash;",
        "- `admin`: foydalanuvchilar va umumiy tizim statistikalarini kuzatish.",
        "",
        "## 2.2. Dasturiy arxitektura",
        "",
        (
            "Tizim ko'p qatlamli arxitektura asosida ishlab chiqilgan. Frontend qismi React va "
            "TypeScript yordamida, backend esa FastAPI asosida yaratilgan. Ma'lumotlar qatlamida "
            "SQLAlchemy modeli ishlatiladi, rivojlantirilgan deploy oqimi uchun Alembic migratsiyalari "
            "va PostgreSQL qo'llab-quvvatlanadi."
        ),
        "",
        "Arxitekturaning asosiy qismlari:",
        "- API routerlar: `health`, `auth`, `patients`, `symptoms`, `diagnoses`, `admin`, `admin_ml`;",
        "- autentifikatsiya: JWT access/refresh tokenlar va session-backed refresh rotation;",
        "- ma'lumotlar bazasi: SQLite dev rejimi va PostgreSQL production yo'nalishi;",
        "- frontend workspace: assessment, review va admin ish maydonlari;",
        "- ML va klinik mantiq qatlami: rule-based engine, Naive Bayes baseline, explainability hisobotlari.",
        "",
        "## 2.3. Ma'lumotlar oqimi va preprocessing",
        "",
        (
            "Tizimga keladigan simptom ma'lumotlari avval canonical schema ga normallashtiriladi, "
            "so'ng feature datasetga o'tkaziladi va train/test split manifest bilan birga saqlanadi. "
            "Bu yondashuv real datasetlarni mapping orqali ulanganda ham pipeline ni bir xil saqlashga yordam beradi."
        ),
        "",
        (
            f"Joriy seed datasetda {dataset['total_rows']} ta yozuv mavjud bo'lib, cleaning reportga ko'ra "
            f"{cleaning['rows_with_any_change']} ta qatorda o'zgarish aniqlangan va "
            f"{cleaning['total_field_changes']} ta maydon transformatsiya qilingan."
        ),
        "",
        "Ko'zga tashlangan data-quality holatlari:",
    ]
    lines.extend(_bullet_lines(quality["warnings"]))
    lines.extend(
        [
            "",
            "Eng ko'p default bilan to'ldirilgan maydonlar:",
        ]
    )
    lines.extend(_top_item_lines(cleaning["top_defaulted_fields"]))
    lines.extend(
        [
            "",
            "## 2.4. Klinik qaror mantiqi va model qatlami",
            "",
            (
                "Dastlabki baholash gibrid yondashuv asosida qurilgan. Bir tomondan, klinik xavf "
                "holatlari uchun rule-based qoidalar ishlaydi. Ikkinchi tomondan, featurelar asosida "
                "categorical Naive Bayes baseline modeli ehtimoliy qo'llab-quvvatlash beradi. "
                "Natijada diagnosis javobida rule signallari va model support birga qaytariladi."
            ),
            "",
            (
                f"Joriy baholash bo'yicha holdout aniqligi {performance['holdout_accuracy']}, "
                f"cross-validation aniqligi esa {performance['cv_accuracy']} ni tashkil etdi. "
                f"Explainability hisobotida {explainability['label_count']} ta sinf va "
                f"{explainability['feature_count']} ta feature qamrab olindi."
            ),
            "",
            "## 2.5. Testlash va deploy tayyorgarligi",
            "",
            (
                "Backend qismida auth, diagnosis, dataset pipeline, explainability, admin va ML oqimlari "
                "uchun avtomatlashtirilgan testlar mavjud. Deploy tomonda Docker Compose, PostgreSQL servisi "
                "va `alembic upgrade head` oqimi tayyorlangan. Frontend esa build bosqichida tekshiriladi."
            ),
            "",
            "## 2.6. Bob bo'yicha xulosa",
            "",
            (
                "Mazkur bobda CDSS tizimining funksional talablari, dasturiy arxitekturasi, "
                "ma'lumotlar oqimi va model qatlamining amaliy tuzilmasi bayon qilindi. "
                "Shu bilan tizim keyingi bosqichda real dataset bilan qayta trening, XGBoost taqqoslash "
                "va klinik workflow chuqurlashtirish uchun tayyor platformaga aylandi."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def build_diploma_conclusion_draft(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    performance = report["performance_summary"]
    explainability = report["explainability_summary"]
    limitations = report["limitations"]
    recommendations = report["recommendations"]

    lines = [
        "# Xulosa",
        "",
        (
            "Diplom ishi doirasida nafas yo'llari infeksiyalari simptomlari asosida dastlabki "
            "baholashni amalga oshiruvchi klinik qarorlarni qo'llab-quvvatlash tizimining ishlaydigan "
            "prototipi yaratildi. Tizimda foydalanuvchini autentifikatsiya qilish, bemor ma'lumotlarini "
            "yuritish, simptomlarni baholash, tashxis natijasini izohlash, shifokor tasdig'i va "
            "administrator monitoringi birlashtirildi."
        ),
        "",
        "Asosiy amaliy natijalar:",
        f"- seed dataset hajmi: {dataset['total_rows']} ta yozuv;",
        f"- sinflar soni: {dataset['total_labels']} ta;",
        f"- holdout accuracy: {performance['holdout_accuracy']};",
        f"- cross-validation accuracy: {performance['cv_accuracy']};",
        f"- explainability qamrovi: {explainability['label_count']} ta sinf va {explainability['feature_count']} ta feature.",
        "",
        (
            "Shu bilan birga, loyiha faqat model yaratish bilan cheklanmay, balki preprocessing, "
            "data quality nazorati, dataset onboarding, cleaning comparison, explainability va "
            "diplom hisobotlarini avtomatik tayyorlash bosqichlarini ham qamrab oldi."
        ),
        "",
        "Ishning asosiy cheklovlari:",
    ]
    lines.extend(_bullet_lines(limitations))
    lines.extend(
        [
            "",
            "Kelgusidagi ustuvor yo'nalishlar:",
        ]
    )
    lines.extend(_bullet_lines(recommendations[:6]))
    lines.extend(
        [
            "",
            (
                "Umuman olganda, ishlab chiqilgan prototip diplom ishining amaliy qismini "
                "shakllantirish uchun yetarli texnik poydevor yaratdi. Keyingi bosqichda real "
                "klinika ma'lumotlari bilan modelni qayta o'qitish, kuchliroq modellar bilan "
                "taqqoslash va klinik ekspertlar bilan validatsiya o'tkazish zarur."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def build_diploma_full_draft(
    chapter_1: str,
    chapter_2: str,
    chapter_3: str,
    conclusion: str,
) -> str:
    return "\n".join(
        [
            "# Diplom Ish Drafti",
            "",
            (
                "Quyidagi matn avtomatik generatsiya qilingan draft bo'lib, diplom talablari bo'yicha "
                "stilistik tahrir, adabiyotlar va rasm-jadvallar bilan boyitilishi kerak."
            ),
            "",
            chapter_1,
            "",
            chapter_2,
            "",
            chapter_3,
            "",
            conclusion,
            "",
        ]
    )


def save_diploma_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
