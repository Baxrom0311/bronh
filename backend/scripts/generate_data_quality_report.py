from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DEFAULT_INPUT_PATH = BASE_DIR / "data" / "respiratory_canonical_dataset.csv"
from app.services.ml_pipeline_service import generate_data_quality_report


def main() -> None:
    input_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_INPUT_PATH
    result = generate_data_quality_report(input_path)
    print(f"Quality JSON saved to: {result['quality_json_path']}")
    print(f"Quality Markdown saved to: {result['quality_markdown_path']}")
    print(f"Warnings: {result['warnings']} | Duplicates: {result['duplicate_rows']}")


if __name__ == "__main__":
    main()
