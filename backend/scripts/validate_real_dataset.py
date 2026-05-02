from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.ml.dataset_onboarding import (
    build_onboarding_validation_report,
    onboarding_report_to_markdown,
    save_onboarding_report_json,
    save_onboarding_report_markdown,
)

DEFAULT_DATASET_PATH = BASE_DIR / "data" / "respiratory_seed_cases.csv"
DEFAULT_MAPPING_PATH = BASE_DIR / "data" / "real_dataset_mapping_template.json"
DEFAULT_OUTPUT_JSON = BASE_DIR / "data" / "real_dataset_validation.json"
DEFAULT_OUTPUT_MD = BASE_DIR / "data" / "real_dataset_validation.md"


def main() -> None:
    dataset_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_DATASET_PATH
    mapping_path = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else DEFAULT_MAPPING_PATH

    report = build_onboarding_validation_report(dataset_path, mapping_path)
    save_onboarding_report_json(DEFAULT_OUTPUT_JSON, report)
    save_onboarding_report_markdown(DEFAULT_OUTPUT_MD, onboarding_report_to_markdown(report))

    print(f"Validation JSON saved to: {DEFAULT_OUTPUT_JSON.relative_to(BASE_DIR)}")
    print(f"Validation Markdown saved to: {DEFAULT_OUTPUT_MD.relative_to(BASE_DIR)}")
    print(f"Ready for pipeline: {report['ready_for_pipeline']}")
    print(f"Missing required fields: {len(report['missing_required_fields'])}")
    print(f"Unused dataset columns: {len(report['unused_dataset_columns'])}")


if __name__ == "__main__":
    main()
