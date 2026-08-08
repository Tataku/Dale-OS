#!/usr/bin/env python3
"""Run one paid behavioral case against one benchmark role.

This is the cost-aware verification path after a narrow skill change. It reuses the
frozen corpus and provider/model resolution contract, but does not rerun unrelated
model slots or evaluation groups.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESILIENT = ROOT / "scripts" / "run_live_model_evals_resilient.py"

spec = importlib.util.spec_from_file_location("dale_live_eval_resilient", RESILIENT)
if spec is None or spec.loader is None:
    raise SystemExit("unable to load live-model evaluator")
wrapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrapper)
base = wrapper.base


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=("openai", "anthropic"), default="openai")
    ap.add_argument("--role", default="balanced")
    ap.add_argument("--case-id", default="systemic-bug-blast-radius")
    ap.add_argument("--out", default="artifacts/live-behavior-probe")
    args = ap.parse_args()

    contract = json.loads((ROOT / "release/live-model-thresholds.json").read_text(encoding="utf-8"))
    cases = base.load_jsonl(ROOT / "evals/behavioral/flagship.jsonl")
    case = next((row for row in cases if row["id"] == args.case_id), None)
    if case is None:
        raise SystemExit(f"unknown behavioral case: {args.case_id}")

    role_spec = next(
        (row for row in contract["models"] if row["provider"] == args.provider and row["role"] == args.role),
        None,
    )
    if role_spec is None:
        raise SystemExit(f"unknown benchmark role: {args.provider}:{args.role}")

    if args.provider == "openai":
        key = os.environ.get("OPENAI_API_KEY", "")
        if not key:
            raise SystemExit("OPENAI_API_KEY is required")
        available = base.openai_models(key)
        model = base.choose_model(role_spec, available, set())
        call = lambda system, user, max_tokens: base.openai_text(key, model, system, user, max_tokens)
    else:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            raise SystemExit("ANTHROPIC_API_KEY is required")
        available = base.anthropic_models(key)
        model = base.choose_model(role_spec, available, set())
        call = lambda system, user, max_tokens: base.anthropic_text(key, model, system, user, max_tokens)

    raw = base.run_behavioral(call, [case])
    scored = base.score_behavioral([case], raw)
    detail = scored["details"][0]
    receipt = {
        "schema": "dale-os/live-behavior-probe/v1",
        "dale_os_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "provider": args.provider,
        "role": args.role,
        "model": model,
        "case_id": args.case_id,
        "skill": case["skill"],
        "frozen_case": {
            "prompt": case["prompt"],
            "must": case["must"],
            "must_not": case["must_not"],
        },
        "lexical_pass": detail["lexical_pass"],
        "missing_required": detail["missing_required"],
        "present_forbidden": detail["present_forbidden"],
        "response": detail["response"],
        "semantic_review_required": True,
        "note": "A targeted probe is evidence collection, not an automatic semantic verdict.",
    }

    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{base.safe_name(args.provider, args.role, model)}--{args.case_id}.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
