from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

MODEL_PATH = BASE_DIR / "ml_models" / "respiratory_nb_model.json"
METRICS_PATH = BASE_DIR / "ml_models" / "respiratory_nb_metrics.json"
from app.services.ml_pipeline_service import train_baseline_model


def main() -> None:
    payload = train_baseline_model()
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")
    print(json.dumps(payload["metrics"], indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
