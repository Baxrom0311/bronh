from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DEFAULT_MODEL_PATH = BASE_DIR / "ml_models" / "respiratory_nb_model.json"
from app.services.ml_pipeline_service import generate_explainability_report


def main() -> None:
    model_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_MODEL_PATH
    result = generate_explainability_report(model_path)
    print(f"Explainability JSON saved to: {result['explainability_json_path']}")
    print(f"Explainability Markdown saved to: {result['explainability_markdown_path']}")
    print(f"Labels: {result['labels']} | Top N: {result['top_n']}")


if __name__ == "__main__":
    main()
