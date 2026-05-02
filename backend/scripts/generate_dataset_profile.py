from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DEFAULT_INPUT_PATH = BASE_DIR / "data" / "respiratory_seed_cases.csv"
from app.services.ml_pipeline_service import generate_dataset_profile


def main() -> None:
    input_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_INPUT_PATH
    mapping_path = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None
    result = generate_dataset_profile(input_path, mapping_path=mapping_path)
    print(f"Profile JSON saved to: {result['profile_json_path']}")
    print(f"Profile Markdown saved to: {result['profile_markdown_path']}")
    print(f"Rows: {result['rows']} | Labels: {result['labels']}")


if __name__ == "__main__":
    main()
