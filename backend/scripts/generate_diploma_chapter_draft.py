from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.ml_pipeline_service import generate_diploma_chapter_draft


def main() -> None:
    result = generate_diploma_chapter_draft()
    print(f"Diploma chapter draft saved to: {result['diploma_chapter_draft_path']}")
    print(f"Source report: {result['source_report_path']}")


if __name__ == "__main__":
    main()
