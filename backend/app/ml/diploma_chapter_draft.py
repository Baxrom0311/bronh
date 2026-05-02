from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _bullet_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- Ma'lumot mavjud emas."]
    return [f"- {item}" for item in items]


def _format_top_items(items: list[dict[str, Any]], suffix: str = "") -> list[str]:
    if not items:
        return ["- Ma'lumot mavjud emas."]
    return [f"- {item['name']}: {item['value']}{suffix}" for item in items]


def _format_signal_lines(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["- Explainability signallari mavjud emas."]
    return [
        (
            f"- {item['label']} sinfi uchun `{item['feature']} = {item['value']}` "
            f"belgisi kuchli signal bo'lib, support={item['support_score']} va lift={item['lift_ratio']}."
        )
        for item in items
    ]


def build_diploma_chapter_draft(report: dict[str, Any]) -> str:
    dataset = report["dataset_summary"]
    quality = report["quality_summary"]
    cleaning = report["cleaning_summary"]
    performance = report["performance_summary"]
    explainability = report["explainability_summary"]
    limitations = report["limitations"]
    recommendations = report["recommendations"]

    lines = [
        "# 3-bob. CDSS modelini ishlab chiqish va baholash natijalari",
        "",
        "## 3.1. Tadqiqot ma'lumotlari tavsifi",
        "",
        (
            "Ushbu bosqichda nafas yo'llari infeksiyalariga oid simptomlar asosida dastlabki "
            "baholashni amalga oshiruvchi model uchun tayyorlangan dataset va undan olingan "
            "natijalar tahlil qilindi."
        ),
        "",
        (
            f"Joriy artefaktlarga ko'ra dataset hajmi {dataset['total_rows']} ta qatorni, "
            f"sinflar soni esa {dataset['total_labels']} tani tashkil etdi. "
            f"Train va test tanlamalari mos ravishda {dataset['train_samples']} va "
            f"{dataset['test_samples']} ta yozuvdan iborat bo'ldi."
        ),
        "",
        "Eng ko'p uchragan sinflar:",
    ]

    lines.extend(_format_top_items(dataset["top_labels"]))
    lines.extend(
        [
            "",
            "Eng ko'p missing kuzatilgan maydonlar:",
        ]
    )
    lines.extend(_format_top_items(dataset["top_missing_fields"]))

    lines.extend(
        [
            "",
            "## 3.2. Preprocessing va data quality bosqichi",
            "",
            (
                "Preprocessing jarayonida ustunlar canonical formatga keltirildi, boolean va enum "
                "qiymatlar normallashtirildi hamda data quality tekshiruvlari bajarildi."
            ),
            "",
            (
                f"Data quality hisobotiga ko'ra duplicate qatorlar soni {quality['duplicate_rows']} ta, "
                f"class balance ratio esa {quality['class_balance_ratio']} ga teng bo'ldi. "
                f"Cleaning report bo'yicha {cleaning['rows_with_any_change']} ta qatorda o'zgarish aniqlanib, "
                f"jami {cleaning['total_field_changes']} ta maydon transformatsiya qilindi."
            ),
            "",
            "Asosiy sifat ogohlantirishlari:",
        ]
    )
    lines.extend(_bullet_lines(quality["warnings"]))
    lines.extend(
        [
            "",
            "Default qiymat bilan to'ldirilgan asosiy maydonlar:",
        ]
    )
    lines.extend(_format_top_items(cleaning["top_defaulted_fields"]))

    lines.extend(
        [
            "",
            "## 3.3. Modelni o'qitish va baholash",
            "",
            (
                "Bazaviy model sifatida categorical Naive Bayes yondashuvi ishlatildi. "
                "Model holdout va cross-validation orqali baholandi."
            ),
            "",
            (
                f"Natijalarga ko'ra holdout aniqligi {performance['holdout_accuracy']}, "
                f"cross-validation aniqligi esa {performance['cv_accuracy']} ni tashkil etdi. "
                f"Baholash {performance['folds']} ta fold asosida amalga oshirildi."
            ),
            "",
            "Per-label bo'yicha eng yaxshi natijalar:",
        ]
    )
    lines.extend(_format_top_items(performance["best_labels"]))

    lines.extend(
        [
            "",
            "[Jadval 3.1 shu yerga qo'yiladi: modelning holdout va cross-validation natijalari]",
            "",
            "## 3.4. Model interpretatsiyasi va explainability",
            "",
            (
                "Model natijalarining tushuntiriluvchanligini oshirish uchun har bir sinf uchun "
                "eng kuchli feature-signallar alohida ajratildi. Ushbu yondashuv klinik qarorni "
                "izohlashda qaysi simptom yoki belgilar kuchliroq ta'sir qilganini ko'rsatadi."
            ),
            "",
            (
                f"Explainability hisobotida {explainability['label_count']} ta sinf va "
                f"{explainability['feature_count']} ta feature qamrab olindi."
            ),
            "",
            "Global explainability highlightlar:",
        ]
    )
    lines.extend(_format_signal_lines(explainability["top_global_signals"]))
    lines.extend(
        [
            "",
            "[Rasm 3.1 shu yerga qo'yiladi: explainability yoki SHAP natijalari]",
            "",
            "## 3.5. Natijalarning cheklovlari",
            "",
            (
                "Olingan natijalarni talqin qilishda quyidagi cheklovlarni hisobga olish zarur. "
                "Ayniqsa, seed dataset sintetik bo'lgani sababli yuqori natijalar real klinik "
                "ma'lumotlarda qayta tekshirilishi kerak."
            ),
            "",
        ]
    )
    lines.extend(_bullet_lines(limitations))
    lines.extend(
        [
            "",
            "## 3.6. Bob bo'yicha xulosa",
            "",
            (
                "Mazkur bobda CDSS tizimi uchun tayyorlangan bazaviy ML pipeline, preprocessing "
                "jarayoni, modelni baholash natijalari va explainability yondashuvi ko'rib chiqildi. "
                "Olingan natijalar prototip darajasida ijobiy bo'lsa-da, keyingi bosqichda real "
                "dataset asosida qayta o'qitish va kuchliroq model bilan taqqoslash talab etiladi."
            ),
            "",
            "Keyingi amaliy tavsiyalar:",
        ]
    )
    lines.extend(_bullet_lines(recommendations[:6]))
    lines.extend(
        [
            "",
            "[Izoh: bu draft matn bo'lib, diplom talablari bo'yicha stilistik tahrir va adabiyotlar bilan boyitilishi kerak.]",
            "",
        ]
    )
    return "\n".join(lines)


def save_diploma_chapter_draft(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
