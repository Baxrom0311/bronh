from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.ml_pipeline_service import generate_diploma_results_report


def main() -> None:
    result = generate_diploma_results_report()
    print(f"Diploma report JSON saved to: {result['diploma_report_path']}")
    print(f"Diploma report Markdown saved to: {result['diploma_report_markdown_path']}")
    print(f"Holdout accuracy: {result['holdout_accuracy']} | CV accuracy: {result['cv_accuracy']}")


if __name__ == "__main__":
    main()
