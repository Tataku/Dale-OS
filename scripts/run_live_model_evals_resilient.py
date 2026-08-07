#!/usr/bin/env python3
"""Compatibility wrapper for provider JSON response shapes.

This does not alter corpora, thresholds, scoring, or skill text. It only unwraps
valid JSON containers returned by providers so the frozen evaluator can score
the same case rows across model families.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "scripts" / "run_live_model_evals.py"

spec = importlib.util.spec_from_file_location("dale_live_eval_base", BASE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("unable to load base live-model evaluator")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
_original_extract_json = base.extract_json


def _find_case_rows(value, depth: int = 0):
    if depth > 3:
        return None
    if isinstance(value, list):
        if all(isinstance(row, dict) for row in value):
            return value
        for item in value:
            found = _find_case_rows(item, depth + 1)
            if found is not None:
                return found
        return None
    if isinstance(value, dict):
        # Common provider wrappers.
        for key in ("results", "cases", "items", "evaluations", "selections", "output", "data"):
            if key in value:
                found = _find_case_rows(value[key], depth + 1)
                if found is not None:
                    return found
        # Some models key each result directly by case id.
        if value and all(isinstance(k, str) and isinstance(v, dict) for k, v in value.items()):
            rows = []
            for case_id, row in value.items():
                normalized = dict(row)
                normalized.setdefault("case_id", case_id)
                rows.append(normalized)
            if all("case_id" in row for row in rows):
                return rows
        for item in value.values():
            found = _find_case_rows(item, depth + 1)
            if found is not None:
                return found
    return None


def resilient_extract_json(text: str):
    parsed = _original_extract_json(text)
    rows = _find_case_rows(parsed)
    if rows is not None:
        return rows
    return parsed


base.extract_json = resilient_extract_json

if __name__ == "__main__":
    base.main()
