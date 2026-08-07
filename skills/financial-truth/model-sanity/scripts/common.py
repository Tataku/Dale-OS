from __future__ import annotations
import json, sys
from decimal import Decimal, InvalidOperation
from datetime import date

def read_json():
    try:
        return json.load(sys.stdin)
    except Exception as exc:
        raise SystemExit(f"invalid JSON input: {exc}")

def emit(value):
    json.dump(value, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")

def dec(value, field="value"):
    if value is None or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric, not {value!r}")
    try:
        return Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be numeric") from exc

def iso_day(value, field="date"):
    try:
        return date.fromisoformat(str(value))
    except Exception as exc:
        raise ValueError(f"{field} must be YYYY-MM-DD") from exc

def money(value: Decimal):
    return float(value.quantize(Decimal('0.01')))
