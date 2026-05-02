from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.ml_pipeline_service import generate_diploma_supporting_drafts


def main() -> None:
    result = generate_diploma_supporting_drafts()
    print(f"Chapter 1 draft saved to: {result['chapter_1_path']}")
    print(f"Chapter 2 draft saved to: {result['chapter_2_path']}")
    print(f"Chapter 3 draft saved to: {result['chapter_3_path']}")
    print(f"Conclusion draft saved to: {result['conclusion_path']}")
    print(f"Full draft saved to: {result['full_draft_path']}")
    print(f"Source report: {result['source_report_path']}")


if __name__ == "__main__":
    main()
