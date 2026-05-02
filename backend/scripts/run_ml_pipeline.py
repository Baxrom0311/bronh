from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DEFAULT_INPUT_PATH = BASE_DIR / "data" / "respiratory_seed_cases.csv"
from app.services.ml_pipeline_service import run_full_ml_pipeline


def main() -> None:
    input_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_INPUT_PATH
    mapping_path = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None
    print(
        json.dumps(
            run_full_ml_pipeline(input_path=input_path, mapping_path=mapping_path),
            indent=2,
            ensure_ascii=True,
        )
    )


if __name__ == "__main__":
    main()
