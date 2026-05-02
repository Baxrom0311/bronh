from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DEFAULT_INPUT_PATH = BASE_DIR / "data" / "respiratory_seed_cases.csv"
from app.services.ml_pipeline_service import generate_cleaning_report


def main() -> None:
    input_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_INPUT_PATH
    mapping_path = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None
    result = generate_cleaning_report(input_path, mapping_path=mapping_path)
    print(f"Cleaning JSON saved to: {result['cleaning_json_path']}")
    print(f"Cleaning Markdown saved to: {result['cleaning_markdown_path']}")
    print(f"Rows with changes: {result['rows_with_any_change']}")
    print(f"Total field changes: {result['total_field_changes']}")


if __name__ == "__main__":
    main()
