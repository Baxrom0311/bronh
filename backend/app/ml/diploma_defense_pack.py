from __future__ import annotations

from pathlib import Path
from typing import Any


def _bullet_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- Ma'lumot mavjud emas."]
    return [f"- {item}" for item in items]


def _top_item_lines(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["- Ma'lumot mavjud emas."]
    return [f"- {item['name']}: {item['value']}" for item in items]


def build_diploma_presentation_outline(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    quality = report["quality_summary"]
    cleaning = report["cleaning_summary"]
    performance = report["performance_summary"]
    explainability = report["explainability_summary"]
    limitations = report["limitations"]
    recommendations = report["recommendations"]

    lines = [
        "# Himoya Uchun Prezentatsiya Rejasi",
        "",
        "## Slayd 1. Mavzu va maqsad",
        "- Mavzu: nafas yo'llari infeksiyalari simptomlari asosida dastlabki baholashni amalga oshiruvchi CDSS",
        "- Maqsad: izohlanadigan va kengaytiriladigan klinik qarorlarni qo'llab-quvvatlash prototipini yaratish",
        "- Natija: web ilova, ML pipeline va diplom hisobot artefaktlari",
        "",
        "## Slayd 2. Muammo va dolzarblik",
        "- Nafas yo'llari kasalliklarida simptomlar o'xshash bo'lishi sababli dastlabki baholash qiyinlashadi",
        "- Birlamchi bo'g'in va skrining bosqichida tezkor, izohlanadigan qaror ko'magi kerak",
        "- Tizim bemorni to'g'ri yo'naltirish va xavfli holatlarni ajratishga yordam beradi",
        "",
        "## Slayd 3. Qo'yilgan vazifalar",
        "- simptomlar va klinik indikatorlarni formal ko'rinishga keltirish",
        "- backend, frontend va ma'lumotlar bazasi arxitekturasini qurish",
        "- rule-based va baseline ML modelni bitta oqimga birlashtirish",
        "- evaluation, explainability va diplom hisobotlarini avtomatlashtirish",
        "",
        "## Slayd 4. Tizim arxitekturasi",
        "- Frontend: React + TypeScript",
        "- Backend: FastAPI + SQLAlchemy + JWT autentifikatsiya",
        "- DB: SQLite dev rejimi, PostgreSQL + Alembic production yo'nalishi",
        "- Rollar: patient, doctor, admin",
        "- API modullar: auth, patients, symptoms, diagnoses, admin, admin_ml",
        "",
        "## Slayd 5. Ma'lumotlar va preprocessing",
        f"- Dataset hajmi: {dataset['total_rows']} ta yozuv",
        f"- Label soni: {dataset['total_labels']} ta",
        f"- Train/Test: {dataset['train_samples']} / {dataset['test_samples']}",
        f"- Cleaning o'zgarishi bo'lgan qatorlar: {cleaning['rows_with_any_change']}",
        f"- Transformatsiya qilingan maydonlar: {cleaning['total_field_changes']}",
        "- Canonical schema, feature dataset va split manifest shakllantirilgan",
        "",
        "Ko'zga tashlangan maydonlar:",
    ]
    lines.extend(_top_item_lines(dataset["top_missing_fields"]))
    lines.extend(
        [
            "",
            "## Slayd 6. Klinik qaror mantiqi",
            "- Rule-based qoidalar xavfli klinik holatlarni ajratadi",
            "- Categorical Naive Bayes baseline model ehtimoliy qo'llab-quvvatlash beradi",
            "- Natijada tashxis, risk darajasi va structured explanation qaytariladi",
            "- Doctor tasdiqlashi va admin monitoringi qo'llab-quvvatlanadi",
            "",
            "## Slayd 7. Baholash natijalari",
            f"- Holdout aniqligi: {performance['holdout_accuracy']}",
            f"- Cross-validation aniqligi: {performance['cv_accuracy']}",
            f"- Fold soni: {performance['folds']}",
            "- Seed datasetda yuqori natija olingan, lekin bu yakuniy klinik xulosa emas",
            "",
            "Eng yaxshi per-label natijalar:",
        ]
    )
    lines.extend(_top_item_lines(performance["best_labels"]))
    lines.extend(
        [
            "",
            "## Slayd 8. Explainability va demo oqimi",
            f"- Explainability qamrovi: {explainability['label_count']} ta sinf, {explainability['feature_count']} ta feature",
            "- UI da symptom assessment, review queue va admin panel mavjud",
            "- Diagnosis javobida rule signals va model support alohida ko'rsatiladi",
            "- Doctor tashxisni tasdiqlashi, admin esa stats va users ni ko'rishi mumkin",
            "",
            "## Slayd 9. Cheklovlar",
        ]
    )
    lines.extend(_bullet_lines(limitations))
    lines.extend(
        [
            "",
            "## Slayd 10. Xulosa va keyingi ishlar",
            "- Prototip darajasidagi CDSS tizimi to'liq ishlaydigan oqimga keltirildi",
            "- ML pipeline, explainability va diplom matn draftlari avtomatlashtirildi",
            "- Keyingi bosqichda real dataset bilan qayta trening va XGBoost taqqoslash zarur",
            "",
            "Keyingi amaliy tavsiyalar:",
        ]
    )
    lines.extend(_bullet_lines(recommendations[:5]))
    return "\n".join(lines) + "\n"


def build_diploma_defense_speech(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    performance = report["performance_summary"]
    explainability = report["explainability_summary"]
    limitations = report["limitations"]
    recommendations = report["recommendations"]

    paragraphs = [
        "# Himoya Uchun Nutq Drafti",
        "",
        (
            "Assalomu alaykum. Mening diplom ish mavzuyim nafas yo'llari infeksiyalari simptomlari "
            "asosida dastlabki baholashni amalga oshiruvchi klinik qarorlarni qo'llab-quvvatlovchi "
            "tizimni ishlab chiqishga bag'ishlangan."
        ),
        "",
        (
            "Mazkur mavzuning dolzarbligi shundaki, nafas yo'llari kasalliklarida ko'plab simptomlar "
            "bir-biriga o'xshash bo'ladi. Shu sababli dastlabki bosqichda bemorning holatini tez va "
            "izohlanadigan tarzda baholash muhim ahamiyatga ega. Ayniqsa, skrining yoki birlamchi bo'g'inda "
            "shifokorga yoki tibbiy xodimga qo'shimcha qaror ko'magi kerak bo'ladi."
        ),
        "",
        (
            "Ishimning asosiy maqsadi simptomlar, hayotiy ko'rsatkichlar va ayrim epidemiologik "
            "omillar asosida dastlabki baholash bera oladigan CDSS prototipini ishlab chiqishdan iborat bo'ldi. "
            "Ushbu maqsadga erishish uchun men backend, frontend, ma'lumotlar bazasi, rule-based qaror qatlami, "
            "baseline ML modeli va explainability mexanizmlarini yagona tizimga birlashtirdim."
        ),
        "",
        (
            "Tizim arxitekturasi amaliy jihatdan uch qismdan iborat. Frontend qismi React va TypeScript "
            "asosida qurilgan bo'lib, unda patient, doctor va admin rollari uchun alohida ish oqimlari mavjud. "
            "Backend qismi FastAPI asosida yozilgan, autentifikatsiya JWT access va refresh tokenlar orqali "
            "amalga oshiriladi. Ma'lumotlar bazasi qatlamida SQLite dev rejimi va PostgreSQL plus Alembic "
            "migratsiya yo'nalishi tayyorlangan."
        ),
        "",
        (
            f"Model va data pipeline bosqichida {dataset['total_rows']} ta yozuv va {dataset['total_labels']} ta "
            "sinfni o'z ichiga olgan seed dataset bilan ishladim. Ma'lumotlar canonical schema ga "
            "normallashtirildi, feature dataset shakllantirildi va train/test split manifest yaratildi. "
            "Shuningdek, dataset profiling, data quality va cleaning reportlar avtomatik generatsiya qilindi."
        ),
        "",
        (
            "Qaror mexanizmi gibrid yondashuv asosida ishlaydi. Bir tomondan, klinik xavf holatlarini "
            "aniqlovchi rule-based qoidalar mavjud. Ikkinchi tomondan, categorical Naive Bayes baseline "
            "modeli ehtimoliy qo'llab-quvvatlash beradi. Natijada tizim foydalanuvchiga nafaqat tashxis "
            "taxminini, balki ushbu natijani qo'llab-quvvatlagan signal va featurelarni ham ko'rsatadi."
        ),
        "",
        (
            f"Baholash natijalariga ko'ra holdout aniqligi {performance['holdout_accuracy']}, "
            f"cross-validation aniqligi esa {performance['cv_accuracy']} ni tashkil etdi. "
            f"Explainability hisobotida {explainability['label_count']} ta sinf va "
            f"{explainability['feature_count']} ta feature qamrab olindi. Bu ko'rsatkichlar prototip "
            "darajasida ijobiy natija berganini ko'rsatadi."
        ),
        "",
        (
            "Shu bilan birga, natijalarni talqin qilishda cheklovlarni hisobga olish zarur. Joriy dataset "
            "kichik va sintetik bo'lgani sababli yuqori accuracy real klinik natija sifatida qabul qilinmaydi. "
            "Buni keyingi bosqichda real ochiq yoki klinik dataset bilan albatta qayta tekshirish kerak."
        ),
        "",
        "Asosiy cheklovlar:",
    ]
    paragraphs.extend(_bullet_lines(limitations))
    paragraphs.extend(
        [
            "",
            (
                "Xulosa qilib aytganda, men diplom ish doirasida ishlaydigan CDSS prototipini yaratdim. "
                "Tizimda foydalanuvchi oqimi, tashxislash, doctor tasdiqlashi, admin monitoringi, ML pipeline, "
                "explainability va diplom hisobotlari birlashtirildi."
            ),
            "",
            "Kelgusidagi ishlar sifatida quyidagilarni rejalashtiraman:",
        ]
    )
    paragraphs.extend(_bullet_lines(recommendations[:5]))
    paragraphs.extend(
        [
            "",
            (
                "E'tiboringiz uchun rahmat. Savollaringiz bo'lsa, mamnuniyat bilan javob beraman."
            ),
            "",
        ]
    )
    return "\n".join(paragraphs)


def save_diploma_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
