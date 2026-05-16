"""Persistence layer for Scenario 2 results."""
import json
from pathlib import Path
from typing import Any


def save_scenario2_result(payload: dict[str, Any], filename: str = "scenario2_result.json") -> Path:
    """Write the scenario 2 result payload to output/data/."""
    target = Path("output/data") / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2))
    return target