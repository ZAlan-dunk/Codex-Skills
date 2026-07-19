#!/usr/bin/env python3
"""Score a planning-to-requirements feature and choose ABC/Enhanced ABC/SDD."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DIMENSIONS = (
    "module_span",
    "data_impact",
    "state_complexity",
    "shared_impact",
    "external_dependency",
    "ambiguity",
    "regression_scope",
)

HARD_TRIGGERS = {
    "persistence_migration",
    "public_framework_change",
    "three_plus_modules",
    "complex_state_machine",
    "external_sdk_or_service",
    "global_concurrency_or_locking",
    "high_cost_core_ambiguity",
    "five_plus_core_scripts",
    "rollback_or_rollout_required",
}


def score(payload: dict) -> dict:
    values = payload.get("dimensions", payload)
    errors = []
    total = 0
    normalized = {}
    for key in DIMENSIONS:
        value = values.get(key, 0)
        if not isinstance(value, int) or value < 0 or value > 2:
            errors.append(f"{key} must be an integer from 0 to 2")
            continue
        normalized[key] = value
        total += value

    hard = sorted(set(payload.get("hard_triggers", [])) & HARD_TRIGGERS)
    unknown_hard = sorted(set(payload.get("hard_triggers", [])) - HARD_TRIGGERS)
    if unknown_hard:
        errors.append("unknown hard triggers: " + ", ".join(unknown_hard))
    if errors:
        raise ValueError("; ".join(errors))

    if hard or total >= 7:
        route = "sdd"
    elif total >= 4:
        route = "enhanced-abc"
    else:
        route = "abc"

    return {
        "score": total,
        "max_score": 14,
        "route": route,
        "hard_triggers": hard,
        "dimensions": normalized,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file path, or '-' for stdin")
    args = parser.parse_args()
    if args.input == "-":
        import sys
        payload = json.load(sys.stdin)
    else:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    print(json.dumps(score(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
